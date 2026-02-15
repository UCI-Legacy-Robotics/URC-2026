#include "arm_hardware_interface/arm_hardware_interface.hpp"

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

namespace arm_hardware_interface
{
// Occurs when initializing the interface, i.e. right away
hardware_interface::CallbackReturn ArmSystemWithODriveAndCubeMars::on_init(
  const hardware_interface::HardwareInfo& info)
{
  // Initialize the parent, checking for success
  if (
    hardware_interface::SystemInterface::on_init(info) !=
    hardware_interface::CallbackReturn::SUCCESS)
  {
    return hardware_interface::CallbackReturn::ERROR;
  }

  // Note info_ is initialized in parent class when on_init is called
  num_joints_ = info_.joints.size();

  hw_positions_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_velocities_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_commands_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());

  for (const hardware_interface::ComponentInfo& joint : info_.joints)
  {
    // Arm has exactly two states and command interfaces on each joint
    if (joint.command_interfaces.size() != 2)
    {
      RCLCPP_FATAL(
        //IMPORTANT note we have to use standalone logger since we aren't in a node
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %zu command interfaces found. 2 expected.",
        joint.name.c_str(), joint.command_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    // Check command interfaces are exactly position and velocity
    if (joint.command_interfaces[0].name != hardware_interface::HW_IF_POSITION)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %s command interface found. '%s' expected.",
        joint.name.c_str(), joint.command_interfaces[0].name.c_str(),
        hardware_interface::HW_IF_POSITION);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.command_interfaces[1].name != hardware_interface::HW_IF_VELOCITY)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %s command interface found. '%s' expected.",
        joint.name.c_str(), joint.command_interfaces[0].name.c_str(),
        hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces.size() != 2)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %zu state interface. 2 expected.", joint.name.c_str(),
        joint.state_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    // Check state interfaces are exactly position and velocity
    if (joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' havs %s state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces[0].name != hardware_interface::HW_IF_VELOCITY)
    {
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %s state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[0].name.c_str(), hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }
  }

  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Initialized arm hardware interface with %zu joints", num_joints_);

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn ArmSystemWithODriveAndCubeMars::on_configure(
  const rclcpp_lifecycle::State& /*previous_state*/)
{
  // Reset values always when configuring hardware
  for (uint i = 0; i < hw_positions_.size(); i++)
  {
    hw_positions_[i] = 0;
    hw_velocities_[i] = 0;
    hw_commands_[i] = 0;
  }
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Successfully configured!");

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Define the state interface that the hardware offers
std::vector<hardware_interface::StateInterface>
ArmSystemWithODriveAndCubeMars::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  for (size_t i = 0; i < num_joints_; i++)
  {
    // StateInterface values are joint name, interface type, and interface value
    // Position interface
    state_interfaces.emplace_back(
      hardware_interface::StateInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_positions_[i]));

    // Velocity interface
    state_interfaces.emplace_back(
      hardware_interface::StateInterface(
        info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &hw_velocities_[i]));
  }

  return state_interfaces;
}

// Define the command interfaces to control the hardware
std::vector<hardware_interface::CommandInterface>
ArmSystemWithODriveAndCubeMars::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  for (size_t i = 0; i < num_joints_; i++)
  {
    command_interfaces.emplace_back(
      hardware_interface::CommandInterface(
        info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &hw_commands_[i]));
  }

  return command_interfaces;
}

// Activate hardware (prepare to be used)
hardware_interface::CallbackReturn
ArmSystemWithODriveAndCubeMars::on_activate(const rclcpp_lifecycle::State& /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Activating hardware");

  //IMPORTANT get a pointer to the arm controller node before creating ROS interfaces
  node_ = std::make_shared<rclcpp::Node>("arm_hardware_interface");

  create_subscribers();
  create_publishers();

  // TODO: zero encoders, read initial states

  // Command and state should be equal when starting
  for (size_t i = 0; i < hw_velocities_.size(); i++)
  {
    hw_commands_[i] = hw_velocities_[i];
  }

  // Start non-blocking executor thread to handle pubs/subs
  executor_ = std::make_shared<rclcpp::executors::SingleThreadedExecutor>();
  executor_->add_node(node_);
  spin_thread = std::thread([this]() { executor_->spin(); });

  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Successfully activated!");

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Deactivate hardware (safely shut donw)
hardware_interface::CallbackReturn
ArmSystemWithODriveAndCubeMars::on_deactivate(const rclcpp_lifecycle::State& /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Deactivating hardware");

  // TODO: stop motors, close connections

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Read hardware states
hardware_interface::return_type ArmSystemWithODriveAndCubeMars::read(
  const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/)
{
  // TODO lock mutex to prevent concurrent reads

  for (size_t i = 0; i < num_joints_; i++)
  {
    // TODO copy feedback buffers over to hw_positions_ and hw_velocities_
  }

  return hardware_interface::return_type::OK;
}

// Write hardware velocity commands
hardware_interface::return_type ArmSystemWithODriveAndCubeMars::write(
  const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/)
{
  // TODO lock mutex to prevent concurrent writes
  
  for (size_t i = 0; i < num_joints_; i++)
  {
    // TODO copy commands from hw_commands_ into cmd_buffer_ to send to hardware nodes
  }

  return hardware_interface::return_type::OK;
}

// Create subscribers to motor statuses
void ArmSystemWithODriveAndCubeMars::create_subscribers()
{
  // Note how mutex is locked as long as the subscription is occurring, and unlocks at the end
  base_sub_ = node_->create_subscription<odrive_can::msg::ControllerStatus>(
    "/base/controller_status", 10,
    [this](const auto & msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      hw_positions_[0] = msg.pos_estimate;
      hw_velocities[0] = msg.vel_estimate;
  });

  shoulder_sub_ = node_->create_subscription<cubemars::msg::ControllerStatus>(
    "/shoulder/controller_status", 10,
    [this](const auto & msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      hw_positions_[1] = msg.pos_estimate_deg;
      hw_velocities[1] = msg.vel_estimate_rpm;
  });

  elbow_sub_ = node_->create_subscription<cubemars::msg::ControllerStatus>(
    "/elbow/controller_status", 10,
    [this](const auto & msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      hw_positions_[2] = msg.pos_estimate_deg;
      hw_velocities[2] = msg.vel_estimate_rpm;
  });

  wrist_pitch_sub_ = node_->create_subscription<cubemars::msg::ControllerStatus>(
    "/wrist_pitch/controller_status", 10,
    [this](const auto & msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      hw_positions_[3] = msg.pos_estimate_deg;
      hw_velocities[3] = msg.vel_estimate_rpm;
  });

  wrist_roll_sub = node_->create_subscription<odrive_can::msg::ControllerStatus>(
    "/wrist_roll/controller_status", 10,
    [this](const auto & msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      hw_positions_[4] = msg.pos_estimate;
      hw_velocities[4] = msg.vel_estimate;
  });

  gripper_sub = node_->create_subscription<odrive_can::msg::ControllerStatus>(
    "/gripper/controller_status", 10,
    [this](const auto & msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      hw_positions_[5] = msg.pos_estimate;
      hw_velocities[5] = msg.vel_estimate;
  });
}

// Create publishers for motor commands
void ArmSystemWithODriveAndCubeMars::create_publishers()
{
  base_pub_ = node->create_publisher<odrive_can::msg::ControlMessage>(
    "/base/control_message", 10
  );

  shoulder_pub_ = node->create_publisher<cubemars_can::msg::ControlMessage>(
    "/shoulder/control_message", 10
  );

  elbow_pub_ = node->create_publisher<cubemars_can::msg::ControlMessage>(
    "/elbow/control_message", 10
  );

  wrist_pitch_pub_ = node->create_publisher<cubemars_can::msg::ControlMessage>(
    "/wrist_pitch/control_message", 10
  );

  wrist_roll_pub_ = node->create_publisher<odrive_can::msg::ControlMessage>(
    "/wrist_roll/control_message", 10
  );

  gripper_pub_ = node->create_publisher<odrive_can::msg::ControlMessage>(
    "/gripper/control_message", 10
  );
}

} // namespace arm_hardware_interface

// Now we need to export this class as a plugin we can use in ros2 control
#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(
  arm_hardware_interface::ArmSystemWithODriveAndCubeMars, hardware_interface::SystemInterface)