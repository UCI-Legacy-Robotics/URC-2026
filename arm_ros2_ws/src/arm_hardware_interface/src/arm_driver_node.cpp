#include "arm_hardware_interface/arm_driver_node.hpp"

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

#define NUM_JOINTS 7

ArmDriverNode::ArmDriverNode()
  : Node("arm_driver_node"), shared_data_(get_arm_shared_data())
  {
    if (!shared_data_) {
      RCLCPP_FATAL(this->get_logger(), "Shared data is null!");
      throw std::runtime_error("Shared data not initialized");
    }

    create_subscribers();
    create_publishers();

    // 100Hz
    command_timer_ = this->create_wall_timer(
      10ms, std::bind(&ArmDriverNode::command_timer_callback, this));

    // 20Hz
    telemetry_timer_ = this->create_wall_timer(
      50ms, std::bind(&ArmDriverNode::telemetry_timer_callback, this));
  }

void ArmDriverNode::command_timer_callback()
{
  // Asynchronously publish command messages to prevent blocking feedback
  std::lock_guard<std::mutex> lock(shared_data_->command_mutex); // Ensure command writing is safe

  // Construct command messages for each motor
  //TODO switch wrist roll and gripper to servo nodes when they are written
  odrive_can::msg::ControlMessage base_msg;
  cubemars_can::msg::ControlMessage shoulder_msg;
  cubemars_can::msg::ControlMessage elbow_msg;
  cubemars_can::msg::ControlMessage wrist_pitch_msg;
  servo::msg::ControlMessage wrist_roll_msg;
  stepper_can::msg::ControlMessage solenoid_msg;
  servo::msg::ControlMessage gripper_msg;

  // Set control modes
  base_msg.control_mode         = 2; // ODrive velocity mode is 2
  shoulder_msg.control_mode     = 3; // CubeMars velocity mode is 3
  elbow_msg.control_mode        = 3;
  wrist_pitch_msg.control_mode  = 3;
  wrist_roll_msg.control_mode   = 0; // Servo velocity mode is 0
  solenoid_msg.control_mode     = 4; // Stepper mode is always 4
  gripper_msg.control_mode      = 0;

  // Set input mode to velocity ramp for odrives
  base_msg.input_mode = 2;
  
  // Set input mode to velocity for stepper
  solenoid_msg.input_mode = 1;

  // Copy in velocity commands from command buffer
  base_msg.input_vel              = shared_data_->commands[0];
  shoulder_msg.input_vel_rpm      = shared_data_->commands[1];
  elbow_msg.input_vel_rpm         = shared_data_->commands[2];
  wrist_pitch_msg.input_vel_rpm   = shared_data_->commands[3];
  wrist_roll_msg.input_vel_deg    = shared_data_->commands[4]; // Servo wants deg/s
  solenoid_msg.input_vel          = static_cast<int>(shared_data_->commands[5]); // Stepper wants int
  gripper_msg.input_vel_deg       = shared_data_->commands[6];

  // Publish messages
  base_pub_->publish(base_msg);
  shoulder_pub_->publish(shoulder_msg);
  elbow_pub_->publish(elbow_msg);
  wrist_pitch_pub_->publish(wrist_pitch_msg);
  wrist_roll_pub_->publish(wrist_roll_msg);
  solenoid_pub_->publish(solenoid_msg);
  gripper_pub_->publish(gripper_msg);
}

void ArmDriverNode::telemetry_timer_callback()
{
  std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex); // Ensure state reading is safe

  arm_hardware_interface::msg::ArmTelemetry msg;

  rclcpp::Time now = this->get_clock()->now();
  msg.header.stamp = now;

  msg.base_position         = shared_data_->position_feedback[0];
  msg.base_velocity         = shared_data_->velocity_feedback[0];
  msg.shoulder_position     = shared_data_->position_feedback[1];
  msg.shoulder_velocity     = shared_data_->velocity_feedback[1];
  msg.elbow_position        = shared_data_->position_feedback[2];
  msg.elbow_velocity        = shared_data_->velocity_feedback[2];
  msg.wrist_pitch_position  = shared_data_->position_feedback[3];
  msg.wrist_pitch_velocity  = shared_data_->velocity_feedback[3];
  msg.wrist_roll_position   = shared_data_->position_feedback[4];
  msg.wrist_roll_velocity   = shared_data_->velocity_feedback[4];
  msg.solenoid_position     = shared_data_->position_feedback[5];
  msg.solenoid_velocity     = shared_data_->velocity_feedback[5];
  msg.gripper_position      = shared_data_->position_feedback[6];
  msg.gripper_velocity      = shared_data_->velocity_feedback[6];

  telemetry_pub_->publish(msg);
}

void ArmDriverNode::create_subscribers()
{
  // Note how mutex is locked as long as the subscription is occurring, and unlocks at the end
  base_sub_ = this->create_subscription<odrive_can::msg::ControllerStatus>(
    "/arm/base/controller_status", 10,
    [this](const odrive_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);
      shared_data_->position_feedback[0] = msg.pos_estimate;
      shared_data_->velocity_feedback[0] = msg.vel_estimate;
  });

  shoulder_sub_ = this->create_subscription<cubemars_can::msg::ControllerStatus>(
    "/arm/shoulder/controller_status", 10,
    [this](const cubemars_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);
      shared_data_->position_feedback[1] = msg.pos_estimate_deg;
      shared_data_->velocity_feedback[1] = msg.vel_estimate_rpm;
  });

  elbow_sub_ = this->create_subscription<cubemars_can::msg::ControllerStatus>(
    "/arm/elbow/controller_status", 10,
    [this](const cubemars_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);
      shared_data_->position_feedback[2] = msg.pos_estimate_deg;
      shared_data_->velocity_feedback[2] = msg.vel_estimate_rpm;
  });

  wrist_pitch_sub_ = this->create_subscription<cubemars_can::msg::ControllerStatus>(
    "/arm/wrist_pitch/controller_status", 10,
    [this](const cubemars_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);
      shared_data_->position_feedback[3] = msg.pos_estimate_deg;
      shared_data_->velocity_feedback[3] = msg.vel_estimate_rpm;
  });

  // wrist_roll_sub_ = this->create_subscription<odrive_can::msg::ControllerStatus>(
  //   "/wrist_roll/controller_status", 10,
  //   [this](const odrive_can::msg::ControllerStatus& msg)
  //   {
  //     std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);
  //     shared_data_->position_feedback[4] = msg.pos_estimate;
  //     shared_data_->velocity_feedback[4] = msg.vel_estimate;
  // });

  solenoid_sub_ = this->create_subscription<stepper_can::msg::ControllerStatus>(
    "/arm/solenoid/controller_status", 10,
    [this](const stepper_can::msg::ControllerStatus& msg)
    {
      std::lock_guard<std::mutex> lock(shared_data_->feedback_mutex);
      shared_data_->position_feedback[5] = msg.pos_estimate;
      shared_data_->velocity_feedback[5] = msg.vel_estimate;
  });
}

void ArmDriverNode::create_publishers()
{
  telemetry_pub_ = this->create_publisher<arm_hardware_interface::msg::ArmTelemetry>(
    "/arm_telemetry", 10
  );

  base_pub_ = this->create_publisher<odrive_can::msg::ControlMessage>(
    "/arm/base/control_message", 10
  );

  shoulder_pub_ = this->create_publisher<cubemars_can::msg::ControlMessage>(
    "/arm/shoulder/control_message", 10
  );

  elbow_pub_ = this->create_publisher<cubemars_can::msg::ControlMessage>(
    "/arm/elbow/control_message", 10
  );

  wrist_pitch_pub_ = this->create_publisher<cubemars_can::msg::ControlMessage>(
    "/arm/wrist_pitch/control_message", 10
  );

  wrist_roll_pub_ = this->create_publisher<servo::msg::ControlMessage>(
    "/arm/wrist_roll/control_message", 10
  );

  solenoid_pub_ = this->create_publisher<stepper_can::msg::ControlMessage>(
    "/arm/solenoid/control_message", 10
  );

  gripper_pub_ = this->create_publisher<servo::msg::ControlMessage>(
    "/arm/gripper/control_message", 10
  );
}

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmDriverNode>());
  rclcpp::shutdown();
  return 0;
}