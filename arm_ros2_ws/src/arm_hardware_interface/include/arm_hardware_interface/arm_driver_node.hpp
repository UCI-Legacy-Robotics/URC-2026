#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/header.hpp"

#include "arm_hardware_interface/shared_data.hpp"
#include "arm_hardware_interface/msg/arm_telemetry.hpp"
#include "cubemars_can/msg/controller_status.hpp"
#include "cubemars_can/msg/control_message.hpp"
#include "odrive_can/msg/o_drive_status.hpp"
#include "odrive_can/msg/controller_status.hpp"
#include "odrive_can/msg/control_message.hpp"
#include "odrive_can/srv/axis_state.hpp"
#include "servo/msg/control_message.hpp"

class ArmDriverNode : public rclcpp::Node
{
  public:
    ArmDriverNode();

  private:
    void command_timer_callback();
    void telemetry_timer_callback();

    void create_subscribers();
    void create_publishers();

    rclcpp::TimerBase::SharedPtr command_timer_;
    rclcpp::TimerBase::SharedPtr telemetry_timer_;
    
    // Feedback and command buffers written by ROS callbacks and write() (belong to motors)
    std::shared_ptr<ArmSharedData> shared_data_;

    // ROS interfaces

    // Subscribers
    rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr base_sub_;
    rclcpp::Subscription<cubemars_can::msg::ControllerStatus>::SharedPtr shoulder_sub_;
    rclcpp::Subscription<cubemars_can::msg::ControllerStatus>::SharedPtr elbow_sub_;
    rclcpp::Subscription<cubemars_can::msg::ControllerStatus>::SharedPtr wrist_pitch_sub_;
    // rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr wrist_roll_sub_;
    rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr gripper_sub_;

    // Publishers
    rclcpp::Publisher<arm_hardware_interface::msg::ArmTelemetry>::SharedPtr telemetry_pub_;
    rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr base_pub_;
    rclcpp::Publisher<cubemars_can::msg::ControlMessage>::SharedPtr shoulder_pub_;
    rclcpp::Publisher<cubemars_can::msg::ControlMessage>::SharedPtr elbow_pub_;
    rclcpp::Publisher<cubemars_can::msg::ControlMessage>::SharedPtr wrist_pitch_pub_;
    rclcpp::Publisher<servo::msg::ControlMessage>::SharedPtr wrist_roll_pub_;
    rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr gripper_pub_;
};