#ifndef ARM_HARDWARE_INTERFACE_HPP_ // Header guard
#define ARM_HARDWARE_INTERFACE_HPP_

#include <chrono>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"

#include "cubemars_can/msg/controller_status.hpp"
#include "cubemars_can/msg/control_message.hpp"
#include "odrive_can/msg/o_drive_status.hpp"
#include "odrive_can/msg/controller_status.hpp"
#include "odrive_can/msg/control_message.hpp"
#include "odrive_can/srv/axis_state.hpp"
#include "servo/msg/control_message.hpp"

#include "rclcpp/clock.hpp"
#include "rclcpp/executors/single_threaded_executor.hpp"
#include "rclcpp/logger.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"

namespace arm_hardware_interface
{

class ArmSystemWithODriveAndCubeMars : public hardware_interface::SystemInterface
{
public:
  RCLCPP_SHARED_PTR_DEFINITIONS(ArmSystemWithODriveAndCubeMars)
  
  // Default constructor declaration
  ArmSystemWithODriveAndCubeMars();

  hardware_interface::CallbackReturn on_init(
    const hardware_interface::HardwareInfo& info) override;

  hardware_interface::CallbackReturn on_configure(
    const rclcpp_lifecycle::State& previous_state) override;

  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

  hardware_interface::CallbackReturn on_activate(
    const rclcpp_lifecycle::State& previous_state) override;

  hardware_interface::CallbackReturn on_deactivate(
    const rclcpp_lifecycle::State& previous_state) override;

  hardware_interface::return_type read(
    const rclcpp::Time& time, const rclcpp::Duration& period) override;

  hardware_interface::return_type write(
    const rclcpp::Time& time, const rclcpp::Duration& period) override;

private:
  void create_subscribers();
  void create_publishers();
  void start_publish_timers();

  // Store the command and state interfaces for the robot (belongs to controller)
  size_t num_joints_;
  std::vector<double> hw_commands_;
  std::vector<double> hw_unused_position_commands_;
  std::vector<double> hw_positions_;
  std::vector<double> hw_velocities_;

  // Feedback and command buffers written by ROS callbacks and write() (belong to motors)
  std::vector<double> position_feedback_;
  std::vector<double> velocity_feedback_;
  std::vector<double> command_buffer_;

  // ROS interfaces
  rclcpp::Node::SharedPtr node_;

  // Subscribers
  rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr base_sub_;
  rclcpp::Subscription<cubemars_can::msg::ControllerStatus>::SharedPtr shoulder_sub_;
  rclcpp::Subscription<cubemars_can::msg::ControllerStatus>::SharedPtr elbow_sub_;
  rclcpp::Subscription<cubemars_can::msg::ControllerStatus>::SharedPtr wrist_pitch_sub_;
  // rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr wrist_roll_sub_;
  rclcpp::Subscription<odrive_can::msg::ControllerStatus>::SharedPtr gripper_sub_;

  // Publishers
  rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr base_pub_;
  rclcpp::Publisher<cubemars_can::msg::ControlMessage>::SharedPtr shoulder_pub_;
  rclcpp::Publisher<cubemars_can::msg::ControlMessage>::SharedPtr elbow_pub_;
  rclcpp::Publisher<cubemars_can::msg::ControlMessage>::SharedPtr wrist_pitch_pub_;
  rclcpp::Publisher<servo::msg::ControlMessage>::SharedPtr wrist_roll_pub_;
  rclcpp::Publisher<odrive_can::msg::ControlMessage>::SharedPtr gripper_pub_;

  // Command publisher timer
  rclcpp::TimerBase::SharedPtr command_timer_;

  // Thread safety
  std::mutex feedback_mutex_;
  std::mutex command_mutex_;
  rclcpp::executors::SingleThreadedExecutor::SharedPtr executor_;
  std::thread spin_thread_;
};

} // namespace arm_hardware_interface

#endif // ARM_HARDWARE_INTERFACE_HPP_