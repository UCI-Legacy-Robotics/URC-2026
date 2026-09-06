#ifndef SERVO_CAN_NODE_HPP
#define SERVO_CAN_NODE_HPP

#include <rclcpp/rclcpp.hpp>
#include <rclcpp/version.h>
#include "servo_can/msg/control_message.hpp"
#include "socket_can.hpp"

#include <mutex>
#include <condition_variable>
#include <array>
#include <algorithm>
#include <linux/can.h>
#include <linux/can/raw.h>

using std::placeholders::_1;
using std::placeholders::_2;

using ControlMessage = servo_can::msg::ControlMessage;

class ServoCanNode : public rclcpp::Node {
public:
    ServoCanNode(const std::string& node_name);
    bool init(EpollEventLoop* event_loop); 
    void deinit();
private:
    void recv_callback(const can_frame& frame);
    void subscriber_callback(const ControlMessage::SharedPtr msg);
    void ctrl_msg_callback();
    inline bool verify_length(const std::string&name, uint8_t expected, uint8_t length);
    
    uint16_t node_id_;
    bool axis_idle_on_shutdown_;
    SocketCanIntf can_intf_ = SocketCanIntf();

    EpollEvent sub_evt_;
    std::mutex ctrl_msg_mutex_;
    ControlMessage ctrl_msg_ = ControlMessage();
    rclcpp::Subscription<ControlMessage>::SharedPtr subscriber_;

};

#endif // SERVO_CAN_NODE_HPP
