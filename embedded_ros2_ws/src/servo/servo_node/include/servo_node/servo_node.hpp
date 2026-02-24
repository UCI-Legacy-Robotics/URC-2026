#ifndef SERVO_NODE_HPP
#define SERVO_NODE_HPP

#include <mutex>

#include "servo/msg/control_message.hpp"
// #include "socket_can.hpp"

#include "rclcpp/clock.hpp"
#include <rclcpp/rclcpp.hpp>

using std::placeholders::_1;
using std::placeholders::_2;

using ControlMessage = servo::msg::ControlMessage;

class ServoNode : public rclcpp::Node {
public:
    ServoNode(const std::string& node_name);
    bool init(/* EpollEventLoop* event_loop */); 
    void deinit();
private:
    // void recv_callback(const can_frame& frame);
    void subscriber_callback(const ControlMessage::SharedPtr msg);
    void control_message_callback();
    void start_velocity_output_timer();
    float get_pwm_from_position(float input_pos_deg);
    
    // Node params
    uint8_t channel_id_;
    bool use_hw_{true};
    uint16_t initial_angle_deg_;
    uint16_t min_angle_deg_;
    uint16_t max_angle_deg_;
    uint16_t min_pwm_micro_s_;
    uint16_t max_pwm_micro_s_;

    // Pseudo-velocity control
    rclcpp::TimerBase::SharedPtr velocity_command_timer_;
    bool send_stepped_position_control_flag_;
    double last_velocity_loop_time_seconds_;
    float current_target_pos_deg_;
    float current_target_vel_deg_;
    
    // EpollEvent subscriber_event_;
    std::mutex control_message_mutex_;
    ControlMessage control_message_ = ControlMessage();
    rclcpp::Subscription<ControlMessage>::SharedPtr subscriber_;
};

#endif // SERVO_NODE_HPP
