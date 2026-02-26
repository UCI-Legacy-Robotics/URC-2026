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

#include "arm_hardware_interface/shared_data.hpp"
#include "arm_hardware_interface/msg/arm_telemetry.hpp"

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
  // Shared data interface with arm_driver_node
  std::shared_ptr<ArmSharedData> shared_data_;
  
  size_t num_joints_;
  std::vector<double> hw_commands_;
  std::vector<double> hw_unused_position_commands_;
  std::vector<double> hw_positions_;
  std::vector<double> hw_velocities_;
};

} // namespace arm_hardware_interface

#endif // ARM_HARDWARE_INTERFACE_HPP_