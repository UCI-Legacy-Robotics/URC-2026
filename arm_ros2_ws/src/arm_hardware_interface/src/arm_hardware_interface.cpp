#include "arm_hardware_interface/arm_hardware_interface.hpp"

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

namespace arm_hardware_interface
{

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
  hw_positions_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_velocities_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_commands_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  hw_unused_position_commands_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  position_feedback_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  velocity_feedback_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());
  command_buffer_.resize(num_joints_, std::numeric_limits<double>::quiet_NaN());

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

  //IMPORTANT get a pointer to the arm controller node before creating ROS interfaces
  if (!node_) {
    node_ = std::make_shared<rclcpp::Node>("arm_hardware_interface_node");
  }
  if (!executor_) {
    executor_ = std::make_shared<rclcpp::executors::SingleThreadedExecutor>();
  }
  
  create_subscribers();
  create_publishers();
  
  // TODO: zero encoders, read initial states
  
  start_publish_timers();

  // Command and state should be equal when starting
  for (size_t i = 0; i < hw_velocities_.size(); i++)
  {
    hw_commands_[i] = hw_velocities_[i];
    hw_unused_position_commands_[i] = hw_positions_[i];
  }
  
  // Start non-blocking executor thread to handle pubs/subs
  executor_->add_node(node_);
  // Guard thread to ensure it's not already running
  if (!spin_thread_.joinable()) {
    spin_thread_ = std::thread([this]() { executor_->spin(); });
  }

  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Hardware successfully activated!");

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Deactivate hardware (safely shut donw)
hardware_interface::CallbackReturn
ArmSystemWithODriveAndCubeMars::on_deactivate(const rclcpp_lifecycle::State& /*previous_state*/)
{
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Deactivating hardware");

  // Stop the executor and join the thread
  if (executor_) {
    executor_->cancel();
  }
  if (spin_thread_.joinable()) {
    spin_thread_.join();
  }

  // Clean up to allow clean re-activation
  executor_.reset();
  
  RCLCPP_INFO(rclcpp::get_logger("arm_hardware_interface"), "Hardware Deactivated.");

  return hardware_interface::CallbackReturn::SUCCESS;
}

// Read hardware states
hardware_interface::return_type ArmSystemWithODriveAndCubeMars::read(
  const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/)
{
  // Lock feedback mutex to prevent race condition
  std::lock_guard<std::mutex> lock(feedback_mutex_);

  for (size_t i = 0; i < num_joints_; i++)
  {
    // Copy feedback buffers over to hw_positions_ and hw_velocities_
    // This allows us to asynchronously get feedback from motors

    // Only update if the feedback is a valid number (not NaN)
    if (!std::isnan(position_feedback_[i])) {
      hw_positions_[i] = position_feedback_[i];
    }
    if (!std::isnan(position_feedback_[i])) {
      hw_velocities_[i] = velocity_feedback_[i];
    }
  }

  return hardware_interface::return_type::OK;
}

// Write hardware velocity commands
hardware_interface::return_type ArmSystemWithODriveAndCubeMars::write(
  const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/)
{
  // Lock mutex to prevent concurrent writes
  std::lock_guard<std::mutex> lock(command_mutex_);
  
  for (size_t i = 0; i < num_joints_; i++)
  {
    // Copy commands from hw_commands_ into command_buffer_ to send to hardware nodes
    // Note this is NOT publishing as we want to be fast; this happens in start_publish_timers()
    command_buffer_[i] = hw_commands_[i];

    //TODO this is where we would implement position control if used
  }

  return hardware_interface::return_type::OK;
}

// Create subscribers to motor statuses
void ArmSystemWithODriveAndCubeMars::create_subscribers()
{
  // Note how mutex is locked as long as the subscription is occurring, and unlocks at the end
  base_sub_ = node_->create_subscription<odrive_can::msg::ControllerStatus>(
    "/base/controller_status", 10,
    [this](const odrive_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      position_feedback_[0] = msg.pos_estimate;
      velocity_feedback_[0] = msg.vel_estimate;
  });

  shoulder_sub_ = node_->create_subscription<cubemars_can::msg::ControllerStatus>(
    "/shoulder/controller_status", 10,
    [this](const cubemars_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      position_feedback_[1] = msg.pos_estimate_deg;
      velocity_feedback_[1] = msg.vel_estimate_rpm;
  });

  elbow_sub_ = node_->create_subscription<cubemars_can::msg::ControllerStatus>(
    "/elbow/controller_status", 10,
    [this](const cubemars_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      position_feedback_[2] = msg.pos_estimate_deg;
      velocity_feedback_[2] = msg.vel_estimate_rpm;
  });

  wrist_pitch_sub_ = node_->create_subscription<cubemars_can::msg::ControllerStatus>(
    "/wrist_pitch/controller_status", 10,
    [this](const cubemars_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      position_feedback_[3] = msg.pos_estimate_deg;
      velocity_feedback_[3] = msg.vel_estimate_rpm;
  });

  // wrist_roll_sub_ = node_->create_subscription<odrive_can::msg::ControllerStatus>(
  //   "/wrist_roll/controller_status", 10,
  //   [this](const odrive_can::msg::ControllerStatus& msg)
  //   {
  //     std::lock_guard<std::mutex> lock(feedback_mutex_);
  //     position_feedback_[4] = msg.pos_estimate;
  //     velocity_feedback_[4] = msg.vel_estimate;
  // });

  gripper_sub_ = node_->create_subscription<odrive_can::msg::ControllerStatus>(
    "/gripper/controller_status", 10,
    [this](const odrive_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_);
      position_feedback_[5] = msg.pos_estimate;
      velocity_feedback_[5] = msg.vel_estimate;
  });
}

// Create publishers for motor commands
void ArmSystemWithODriveAndCubeMars::create_publishers()
{
  telemetry_pub_ = node_->create_publisher<arm_hardware_interface::msg::ArmTelemetry>(
    "/arm_telemetry", 10
  );

  base_pub_ = node_->create_publisher<odrive_can::msg::ControlMessage>(
    "/base/control_message", 10
  );

  shoulder_pub_ = node_->create_publisher<cubemars_can::msg::ControlMessage>(
    "/shoulder/control_message", 10
  );

  elbow_pub_ = node_->create_publisher<cubemars_can::msg::ControlMessage>(
    "/elbow/control_message", 10
  );

  wrist_pitch_pub_ = node_->create_publisher<cubemars_can::msg::ControlMessage>(
    "/wrist_pitch/control_message", 10
  );

  wrist_roll_pub_ = node_->create_publisher<servo::msg::ControlMessage>(
    "/wrist_roll/control_message", 10
  );

  gripper_pub_ = node_->create_publisher<odrive_can::msg::ControlMessage>(
    "/gripper/control_message", 10
  );
}

void ArmSystemWithODriveAndCubeMars::start_publish_timers()
{
  // Asynchronously publish command messages to prevent blocking feedback
  command_timer_ = node_->create_wall_timer(
    std::chrono::milliseconds(10), // 100Hz
    [this]()
    {
      std::lock_guard<std::mutex> lock(command_mutex_); // Ensure command writing is safe

      // Construct command messages for each motor
      //TODO switch wrist roll and gripper to servo nodes when they are written
      odrive_can::msg::ControlMessage base_msg;
      cubemars_can::msg::ControlMessage shoulder_msg;
      cubemars_can::msg::ControlMessage elbow_msg;
      cubemars_can::msg::ControlMessage wrist_pitch_msg;
      servo::msg::ControlMessage wrist_roll_msg;
      odrive_can::msg::ControlMessage gripper_msg;

      // Set control modes
      base_msg.control_mode         = 2; // ODrive velocity mode is 2
      shoulder_msg.control_mode     = 3; // CubeMars velocity mode is 3
      elbow_msg.control_mode        = 3;
      wrist_pitch_msg.control_mode  = 3;
      wrist_roll_msg.control_mode   = 0; // Servo velocity mode is 0
      gripper_msg.control_mode      = 2;

      // Set input mode to velocity ramp for odrives
      base_msg.input_mode       = 2;
      // wrist_roll_msg.input_mode = 2;
      gripper_msg.input_mode    = 2;

      // Copy in velocity commands from command buffer
      base_msg.input_vel              = command_buffer_[0];
      shoulder_msg.input_vel_rpm      = command_buffer_[1];
      elbow_msg.input_vel_rpm         = command_buffer_[2];
      wrist_pitch_msg.input_vel_rpm   = command_buffer_[3];
      wrist_roll_msg.input_vel_deg    = command_buffer_[4]; // Servo wants deg/s
      gripper_msg.input_vel           = command_buffer_[5];

      // Publish messages
      base_pub_->publish(base_msg);
      shoulder_pub_->publish(shoulder_msg);
      elbow_pub_->publish(elbow_msg);
      wrist_pitch_pub_->publish(wrist_pitch_msg);
      wrist_roll_pub_->publish(wrist_roll_msg);
      gripper_pub_->publish(gripper_msg);
    }
  );

  // Send telemetry
  telemetry_timer_ = node_->create_wall_timer(
    std::chrono::milliseconds(50), // 20Hz
    [this]()
    {
      std::lock_guard<std::mutex> lock(feedback_mutex_); // Ensure state reading is safe

      arm_hardware_interface::msg::ArmTelemetry msg;

      msg.base_position         = position_feedback_[0];
      msg.base_velocity         = velocity_feedback_[0];
      msg.shoulder_position     = position_feedback_[1];
      msg.shoulder_velocity     = velocity_feedback_[1];
      msg.elbow_position        = position_feedback_[2];
      msg.elbow_velocity        = velocity_feedback_[2];
      msg.wrist_pitch_position  = position_feedback_[3];
      msg.wrist_pitch_velocity  = velocity_feedback_[3];
      msg.wrist_roll_position   = position_feedback_[4];
      msg.wrist_roll_velocity   = velocity_feedback_[4];
      msg.solenoid_position     = position_feedback_[5];
      msg.solenoid_velocity     = velocity_feedback_[5];
      msg.gripper_position      = position_feedback_[6];
      msg.gripper_velocity      = velocity_feedback_[6];

      telemetry_pub_->publish(msg);
    }
  );
}

} // namespace arm_hardware_interface

// Now we need to export this class as a plugin we can use in ros2 control
#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(
  arm_hardware_interface::ArmSystemWithODriveAndCubeMars,
  hardware_interface::SystemInterface
)