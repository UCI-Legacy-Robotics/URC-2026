#include "odrive_can_node.hpp"
#include "odrive_enums.h"
#include "epoll_event_loop.hpp"
#include "byte_swap.hpp"
#include <sys/eventfd.h>
#include <chrono>

enum CmdId : uint32_t {
    kGetControllerData = 0x29,
    kSetVelocityControl = 0x03,
    kSetPositionControl = 0x04,
    kSetOriginMode = 0x05,
    kSetPositionVelocityMode = 0x06
};

ODriveCanNode::ODriveCanNode(const std::string& node_name) : rclcpp::Node(node_name) {
    
    rclcpp::Node::declare_parameter<std::string>("interface", "can0");
    rclcpp::Node::declare_parameter<uint16_t>("node_id", 0);
    rclcpp::Node::declare_parameter<uint8_t>("pole_pairs", 14);

    rclcpp::QoS ctrl_stat_qos(rclcpp::KeepAll{});
    ctrl_publisher_ = rclcpp::Node::create_publisher<ControllerStatus>("controller_status", ctrl_stat_qos);

    rclcpp::QoS ctrl_msg_qos(rclcpp::KeepAll{});
    subscriber_ = rclcpp::Node::create_subscription<ControlMessage>("control_message", ctrl_msg_qos, std::bind(&ODriveCanNode::subscriber_callback, this, _1));
}

void ODriveCanNode::deinit() {
    sub_evt_.deinit();
    can_intf_.deinit();
}

bool ODriveCanNode::init(EpollEventLoop* event_loop) {

    node_id_ = rclcpp::Node::get_parameter("node_id").as_int();
    pole_pairs = rclcpp::Node::get_parameter("pole_pairs").as_bool();
    std::string interface = rclcpp::Node::get_parameter("interface").as_string();

    if (!can_intf_.init(interface, event_loop, std::bind(&ODriveCanNode::recv_callback, this, _1))) {
        RCLCPP_ERROR(rclcpp::Node::get_logger(), "Failed to initialize socket can interface: %s", interface.c_str());
        return false;
    }
    if (!sub_evt_.init(event_loop, std::bind(&ODriveCanNode::ctrl_msg_callback, this))) {
        RCLCPP_ERROR(rclcpp::Node::get_logger(), "Failed to initialize subscriber event");
        return false;
    }

    RCLCPP_INFO(rclcpp::Node::get_logger(), "node_id: %d", node_id_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "interface: %s", interface.c_str());
    return true;
}

void ODriveCanNode::recv_callback(const can_frame& frame) {
    // Ensure extended frame nd lower 8 bits representing node id match
    if((!(frame.can_id & CAN_EFF_FLAG)) || ((frame.can_id & 0xFF) != node_id_)) return;

    // Bits 8 to 29 are command ID
    switch((frame.can_id & 0x1FFFFF00) >> 8) {
        case CmdId::kGetControllerData: {
            if (!verify_length("kControllerData", 8, frame.can_dlc)) break;
            std::lock_guard<std::mutex> guard(ctrl_stat_mutex_);
            ctrl_stat_.pos_estimate_deg     = static_cast<float>(read_le<int16_t>(frame.data + 0)) / 10;
            ctrl_stat_.vel_estimate_rpm     = static_cast<float>(read_le<int16_t>(frame.data + 2)) * 10 / pole_pairs;
            ctrl_stat_.motor_current_amps   = static_cast<float>(read_le<int16_t>(frame.data + 4)) / 100;
            ctrl_stat_.motor_temperature_c  = read_le<int8_t>(frame.data + 6);
            ctrl_stat_.active_errors        = read_le<uint8_t>(frame.data + 7);

            ctrl_pub_flag_ = 1;
            break;
        }
        case CmdId::kSetOriginMode:
        case CmdId::kSetPositionControl:
        case CmdId::kSetPositionVelocityMode:
        case CmdId::kSetVelocityControl: {
            break; // Ignore commands coming from another master/host on the bus
        }
        default: {
            RCLCPP_WARN(rclcpp::Node::get_logger(), "Received unused message: ID = 0x%x", (frame.can_id & 0x1F));
            break;
        }
    }

    // Only publish received status messages
    if (ctrl_pub_flag_ == 1) {
        ctrl_publisher_->publish(ctrl_stat_);
        ctrl_pub_flag_ = 0;
    }
    
}

void ODriveCanNode::subscriber_callback(const ControlMessage::SharedPtr msg) {
    std::lock_guard<std::mutex> guard(ctrl_msg_mutex_);
    ctrl_msg_ = *msg;
    sub_evt_.set();
}

void ODriveCanNode::ctrl_msg_callback() {

    uint32_t control_mode;
    struct can_frame frame;
    {
        std::lock_guard<std::mutex> guard(ctrl_msg_mutex_);
        control_mode = ctrl_msg_.control_mode;
    }

    switch (control_mode) {
        case CmdId::kSetVelocityControl: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "input_vel");
            // Upper bytes are control message, lower byte is node id, MSB is extended frame flag
            frame.can_id = node_id_ | kSetVelocityControl << 8 | CAN_EFF_FLAG;
            std::lock_guard<std::mutex> guard(ctrl_msg_mutex_); 
            int32_t conv_vel_erpm = static_cast<int32_t>(ctrl_msg_.input_vel_rpm * pole_pairs);
            write_le<int32_t>(conv_vel_erpm, frame.data);
            frame.can_dlc = 4;
            return;
        }
        case CmdId::kSetPositionControl: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "input_position");
            frame.can_id = node_id_ | kSetPositionControl << 8 | CAN_EFF_FLAG;
            int32_t conv_pos_motor = static_cast<int32_t>(ctrl_msg_.input_pos_deg * 10000);
            write_le<int32_t>(conv_pos_motor, frame.data);
            frame.can_dlc = 4;
            break;
        }
        case CmdId::kSetOriginMode: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "set_position");
            frame.can_id = node_id_ | kSetOriginMode << 8 | CAN_EFF_FLAG;
            write_le<uint8_t>(ctrl_msg_.set_origin, frame.data);
            frame.can_dlc = 1;
            break;
        }
        case CmdId::kSetPositionVelocityMode: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "input_position_vel");
            frame.can_id = node_id_ | kSetPositionVelocityMode << 8 | CAN_EFF_FLAG;
            std::lock_guard<std::mutex> guard(ctrl_msg_mutex_);
            int32_t conv_pos_motor = static_cast<int32_t>(ctrl_msg_.input_pos_deg * 10000);
            int16_t conv_vel_motor = static_cast<int16_t>(ctrl_msg_.set_vel_limit_rpm * pole_pairs / 10);
            int16_t conv_accel_motor = static_cast<int16_t>(ctrl_msg_.set_accel_limit_rpm_s * pole_pairs / 10);

            write_le<int32_t>(conv_pos_motor,   frame.data);
            write_le<int16_t>(conv_vel_motor,   frame.data + 4);
            write_le<int16_t>(conv_accel_motor, frame.data + 6);
            frame.can_dlc = 8;
            break;
        }    
        case CmdId::kGetControllerData: {
            break;
        }
        default: 
            RCLCPP_ERROR(rclcpp::Node::get_logger(), "unsupported control_mode: %d", control_mode);
            return;
    }

    can_intf_.send_can_frame(frame);
}

inline bool ODriveCanNode::verify_length(const std::string&name, uint8_t expected, uint8_t length) {
    bool valid = expected == length;
    RCLCPP_DEBUG(rclcpp::Node::get_logger(), "received %s", name.c_str());
    if (!valid) RCLCPP_WARN(rclcpp::Node::get_logger(), "Incorrect %s frame length: %d != %d", name.c_str(), length, expected);
    return valid;
}
