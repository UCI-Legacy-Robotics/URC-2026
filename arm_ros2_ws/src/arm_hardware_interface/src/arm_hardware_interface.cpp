#include "arm_hardware_interface/arm_hardware_interface.hpp"

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

namespace arm_hardware_interface
{

constexpr double COMMAND_PUBLISH_RATE_HZ = 100.0;
constexpr double TELEMETRY_PUBLISH_RATE_HZ = 20.0;

// Define gear ratios
constexpr double BASE_GEAR_RATIO = 4.0; // 4:1 gearbox
constexpr double SHOULDER_GEAR_RATIO = 15.0 * 36.0; // 15:1 gearbox, 36:1 in Cubemars
constexpr double ELBOW_GEAR_RATIO = 9.2 * 36.0; // 9.2:1 cables, 36:1 cubemars
constexpr double WRIST_PITCH_GEAR_RATIO = 3.25 * 36.0; // 3.25:1 cables, 36:1 cubemars
constexpr double WRIST_ROLL_GEAR_RATIO = 1.0; // Direct drive
constexpr double SOLENOID_LINEAR_ACTUATOR_GEAR_RATIO = 1.0; // Direct drive
constexpr double GRIPPER_GEAR_RATIO = 1.0; // Direct drive

ArmSystemWithODriveAndCubeMars::ArmSystemWithODriveAndCubeMars() 
{}

// Occurs when initializing the interface, i.e. right away
hardware_interface::CallbackReturn ArmSystemWithODriveAndCubeMars::on_init(
  const hardware_interface::HardwareInfo& info)
{
  // for (int i = 0; i < 10; i++) {
  //   std::cout << "Hello ROS2!" << std::endl;
  // }

  // Initialize the parent, checking for success
  if (
    hardware_interface::SystemInterface::on_init(info) !=
    hardware_interface::CallbackReturn::SUCCESS)
  {
    std::cerr << "Hardware interface superclass failed to init!" << std::endl;
    return hardware_interface::CallbackReturn::ERROR;
  }

  // Note info_ is initialized in parent class when on_init is called
  num_joints_ = info_.joints.size();

  // Resize vectors so they can fit all our values later
  shared_data_ = get_arm_shared_data();

  hw_positions_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_velocities_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_commands_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_unused_position_commands_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());

  // Define hardware gear ratios
  hw_gear_ratios_.push_back(BASE_GEAR_RATIO);
  hw_gear_ratios_.push_back(SHOULDER_GEAR_RATIO);
  hw_gear_ratios_.push_back(ELBOW_GEAR_RATIO);
  hw_gear_ratios_.push_back(WRIST_PITCH_GEAR_RATIO);
  hw_gear_ratios_.push_back(WRIST_ROLL_GEAR_RATIO);
  hw_gear_ratios_.push_back(SOLENOID_LINEAR_ACTUATOR_GEAR_RATIO);
  hw_gear_ratios_.push_back(GRIPPER_GEAR_RATIO);

  for (const hardware_interface::ComponentInfo& joint : info_.joints)
  {
    // Arm has exactly two states and command interfaces on each joint
    if (joint.command_interfaces.size() != 2)
    {
      for (int i = 0; i < 10; i++) {
        std::cerr << "Joint " << joint.name.c_str() << " has " << joint.command_interfaces.size() << "command interfaces found. 2 expected." << std::endl;
      }
      RCLCPP_FATAL(
        //IMPORTANT note we have to use standalone logger since we aren't in a node
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %zu command interfaces found. 2 expected.",
        joint.name.c_str(), joint.command_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    // Check command interfaces are exactly position and velocity
    if (joint.command_interfaces[0].name != hardware_interface::HW_IF_POSITION)
    {
      for (int i = 0; i < 10; i++) {
        std::cerr << "Joint " << joint.name.c_str() << " has " << joint.command_interfaces[0].name.c_str() << " command interface found. Position expected." << std::endl;
      }
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %s command interface found. '%s' expected.",
        joint.name.c_str(), joint.command_interfaces[0].name.c_str(),
        hardware_interface::HW_IF_POSITION);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.command_interfaces[1].name != hardware_interface::HW_IF_VELOCITY)
    {
      for (int i = 0; i < 10; i++) {
        std::cerr << "Joint " << joint.name.c_str() << " has " << joint.command_interfaces[1].name.c_str() << " command interface found. Velocity expected." << std::endl;
      }
        RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %s command interface found. '%s' expected.",
        joint.name.c_str(), joint.command_interfaces[1].name.c_str(),
        hardware_interface::HW_IF_VELOCITY);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces.size() != 2)
    {
      for (int i = 0; i < 10; i++) {
        std::cerr << "Joint " << joint.name.c_str() << " has " << joint.state_interfaces.size() << " state interfaces found. 2 expected." << std::endl;
      }
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %zu state interface. 2 expected.", joint.name.c_str(),
        joint.state_interfaces.size());
      return hardware_interface::CallbackReturn::ERROR;
    }

    // Check state interfaces are exactly position and velocity
    if (joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION)
    {
      for (int i = 0; i < 10; i++) {
        std::cerr << "Joint " << joint.name.c_str() << " has " << joint.state_interfaces[0].name.c_str() << " state interface found. Position expected." << std::endl;
      }
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' havs %s state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
      return hardware_interface::CallbackReturn::ERROR;
    }

    if (joint.state_interfaces[1].name != hardware_interface::HW_IF_VELOCITY)
    {
      for (int i = 0; i < 10; i++) {
        std::cerr << "Joint " << joint.name.c_str() << " has " << joint.state_interfaces[1].name.c_str() << " state interface found. Velocity expected." << std::endl;
      }
      RCLCPP_FATAL(
        rclcpp::get_logger("arm_hardware_interface"), "Joint '%s' has %s state interface. '%s' expected.", joint.name.c_str(),
        joint.state_interfaces[1].name.c_str(), hardware_interface::HW_IF_VELOCITY);
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
    hw_unused_position_commands_[i] = 0;
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

  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Exporting %zu state interfaces", state_interfaces.size());

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

    // Just to make sure we fulfill promise of position commands; unused as of now
    command_interfaces.emplace_back(
      hardware_interface::CommandInterface(
        info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_unused_position_commands_[i]));
  }

  return command_interfaces;
}

// Activate hardware (prepare to be used)
hardware_interface::CallbackReturn
ArmSystemWithODriveAndCubeMars::on_activate(const rclcpp_lifecycle::State& /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Activating hardware");
  
  // TODO: zero encoders, read initial states

  // Command and state should be equal when starting
  for (size_t i = 0; i < hw_velocities_.size(); i++)
  {
    hw_commands_[i] = hw_velocities_[i];
    hw_unused_position_commands_[i] = hw_positions_[i];
  }

  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Hardware successfully activated!");

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Deactivate hardware (safely shut donw)
hardware_interface::CallbackReturn
ArmSystemWithODriveAndCubeMars::on_deactivate(const rclcpp_lifecycle::State& /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Deactivating hardware");

  
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Hardware Deactivated.");

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Read hardware states
hardware_interface::return_type ArmSystemWithODriveAndCubeMars::read(
  const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/)
{
  // Lock feedback mutex to prevent race condition
  std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);

  for (size_t i = 0; i < num_joints_; i++)
  {
    // Copy feedback buffers over to hw_positions_ and hw_velocities_
    // This allows us to asynchronously get feedback from motors

    // Only update if the feedback is a valid number (not NaN)
    // Note that gear ratios are divided since encoders report before gearing
    if (!std::isnan(shared_data_->position_feedback[i])) {
      hw_positions_[i] = shared_data_->position_feedback[i] / hw_gear_ratios_[i];
    }
    if (!std::isnan(shared_data_->velocity_feedback[i])) {
      hw_velocities_[i] = shared_data_->velocity_feedback[i] / hw_gear_ratios_[i];
    }
  }

  // Publish telemetry and hardware feedback data

  return hardware_interface::return_type::OK;
}

// Write hardware velocity commands
hardware_interface::return_type ArmSystemWithODriveAndCubeMars::write(
  const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/)
{
  // Lock mutex to prevent concurrent writes
  std::lock_guard<std::mutex> lock(shared_data_->command_mutex);
  
  for (size_t i = 0; i < num_joints_; i++)
  {
    // Copy commands from hw_commands_ into command_buffer_ to send to hardware nodes
    // Note this is NOT publishing as we need to be fast and non-blocking; this happens in driver node
    // Multiplied by gear ratio since encoder reports before gearing
    shared_data_->commands[i] = hw_commands_[i] * hw_gear_ratios_[i];

    //TODO this is where we would implement position control if used
  }

  return hardware_interface::return_type::OK;
}

} // namespace arm_hardware_interface

// Now we need to export this class as a plugin we can use in ros2 control
#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(
  arm_hardware_interface::ArmSystemWithODriveAndCubeMars,
  hardware_interface::SystemInterface
)