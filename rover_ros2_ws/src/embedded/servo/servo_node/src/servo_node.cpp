#include "servo_node/servo_node.hpp"
// #include "epoll_event_loop.hpp"
#include <chrono>

enum CommandType : uint8_t {
    kVelocityControl = 0,
    kPositionControl = 1
};

ServoNode::ServoNode(const std::string& node_name) : rclcpp::Node(node_name) {
    
    rclcpp::Node::declare_parameter<uint8_t>("channel_id", 0);
    rclcpp::Node::declare_parameter<uint16_t>("initial_angle_deg", 0);
    rclcpp::Node::declare_parameter<uint16_t>("min_angle_deg", 0);
    rclcpp::Node::declare_parameter<uint16_t>("max_angle_deg", 360);
    rclcpp::Node::declare_parameter<uint16_t>("min_pwm_micro_s", 500);
    rclcpp::Node::declare_parameter<uint16_t>("max_pwm_micro_s", 2500);

    rclcpp::QoS control_message_qos(rclcpp::KeepAll{});
    subscriber_ = rclcpp::Node::create_subscription<ControlMessage>("control_message", control_message_qos, std::bind(&ServoNode::subscriber_callback, this, _1));
}

void ServoNode::deinit() {
    // sub_evt_.deinit();
}

bool ServoNode::init(/* EpollEventLoop* event_loop */) {
    // Get node interface for velocity loop timer
    if (!node_) {
        node_ = std::make_shared<rclcpp::Node>("servo_node");
    }

    channel_id_         = rclcpp::Node::get_parameter("channel_id").as_int();
    initial_angle_deg_  = rclcpp::Node::get_parameter("initial_angle_deg").as_int();
    min_angle_deg_      = rclcpp::Node::get_parameter("min_angle_deg").as_int();
    max_angle_deg_      = rclcpp::Node::get_parameter("max_angle_deg").as_int();
    min_pwm_micro_s_    = rclcpp::Node::get_parameter("min_pwm_micro_s").as_int();
    max_pwm_micro_s_    = rclcpp::Node::get_parameter("max_pwm_micro_s").as_int();

    // Set current target position to initial angle
    current_target_pos_deg_ = static_cast<float>(initial_angle_deg_);
    send_stepped_position_control_flag_ = false;
    last_velocity_loop_time_seconds_ = node_->get_clock()->now().seconds();

    // if (!sub_evt_.init(event_loop, std::bind(&CubemarsCanNode::ctrl_msg_callback, this))) {
    //     RCLCPP_ERROR(rclcpp::Node::get_logger(), "Failed to initialize subscriber event");
    //     return false;
    // }

    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo channel_id: %d", channel_id_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo initial_angle_deg: %d", initial_angle_deg_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo min_angle_deg: %d", min_angle_deg_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo max_angle_deg: %d", max_angle_deg_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo min_pwm_micro_s: %d", min_pwm_micro_s_);
    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo max_pwm_micro_s: %d", max_pwm_micro_s_);

    // Start velocity loop timer
    start_velocity_output_timer();

    RCLCPP_INFO(rclcpp::Node::get_logger(), "Servo successfully initialized!");

    return true;
}

void ServoNode::subscriber_callback(const ControlMessage::SharedPtr msg) {
    std::lock_guard<std::mutex> guard(control_message_mutex_);
    control_message_ = *msg;
    // sub_evt_.set();
}

void ServoNode::control_message_callback() {
    ControlMessage locked_msg;
    {
        std::lock_guard<std::mutex> guard(control_message_mutex_);
        locked_msg = control_message_;
    }

    // By default, don't send constant position commands (only for velocity mode)
    send_stepped_position_control_flag_ = false;

    switch (locked_msg.control_mode) {
        case CommandType::kVelocityControl: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "Servo velocity input: %.2f", locked_msg.input_vel_deg);

            // Reset timer so we don't see a huge position jump
            last_velocity_loop_time_seconds_ = node_->get_clock()->now().seconds();
            
            // Convert pseudo-velocity to position control by stepping target position
            // Set velocity for future updates
            current_target_vel_deg_ = locked_msg.input_vel_deg;

            // Convert position from pseudo-velocity loop to pwm
            float pwm = get_pwm_from_position(current_target_pos_deg_);
            
            // Enable repeated position streaming when in velocity mode
            send_stepped_position_control_flag_ = true;

            //TODO copy target pwm into an output message to the driver

            break;
        }
        case CommandType::kPositionControl: {
            RCLCPP_DEBUG(rclcpp::Node::get_logger(), "Servo position input: %.2f", locked_msg.input_pos_deg);
            
            // Convert position to pwm
            float pwm = get_pwm_from_position(locked_msg.input_pos_deg);

            //TODO copy this target pwm into an output message to the driver

            break;
        }
        default: 
            RCLCPP_ERROR(rclcpp::Node::get_logger(), "Unsupported control_mode: %d", locked_msg.control_mode);
            return;
    }

    //TODO send message to servo driver
}

float ServoNode::get_pwm_from_position(float input_pos_deg) {
    // Convert degree position input to pwm output
    // Example implementation:
    // Get target angle as fraction of allowed movement range
    // E.g. for target deg 270, min angle 180 max angle 360, 
    // target_pos_fractional = (270 - 180) / (360 - 180) = 0.5
    double target_pos_fractional = ((input_pos_deg - min_angle_deg_) / 
                                        static_cast<double>(max_angle_deg_ - min_angle_deg_));

    // Now we find the PWM output corresponding to this fraction of the PWM range
    // E.g. for target_pos_fractional 0.5, min pwm 500, max pwm 2500,
    // target_pwm_micro_s = 500 + 0.5 * (2500 - 500) = 1500
    float target_pwm_micro_s = static_cast<float>(min_pwm_micro_s_ + target_pos_fractional *
                                    (max_pwm_micro_s_ - min_pwm_micro_s_));

    return target_pwm_micro_s;
}

void ServoNode::start_velocity_output_timer() {
    // Asynchronously publish position command messages
    velocity_command_timer_ = node_->create_wall_timer(
        std::chrono::milliseconds(20), // 50Hz
        [this]()
        {
            // Return early if we aren't in velocity control mode, as there is no need
            // to continously publish position
            if (!send_stepped_position_control_flag_) {
                return;
            }

            std::lock_guard<std::mutex> guard(control_message_mutex_); // Ensure safe command writing

            // Step target position by velocity * time between loops
            double elapsed_time_seconds = node_->get_clock()->now().seconds() - last_velocity_loop_time_seconds_;
            last_velocity_loop_time_seconds_ = node_->get_clock()->now().seconds();

            current_target_pos_deg_ += current_target_vel_deg_ * elapsed_time_seconds;

            float pwm = get_pwm_from_position(current_target_pos_deg_);

            //TODO write out pwm command to servo driver
        }
    );
}