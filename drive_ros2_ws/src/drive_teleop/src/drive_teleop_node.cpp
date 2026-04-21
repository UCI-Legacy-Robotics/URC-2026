#include <rclcpp/rclcpp.hpp>
#include "drive_teleop/drive_teleop_node.hpp"
#include <iostream>

// Define constants
constexpr int AXIS_COUNT = 8;
constexpr int BUTTON_COUNT = 14;
constexpr size_t ROS_QUEUE_SIZE = 10;

const std::string DRIVE_OUT_TOPIC = "/drive_teleop_node/command";
const std::string DRIVE_FRAME_ID = "drive";

constexpr int MAX_DRIVE_PWM = 32000;

// Buttons and axes
constexpr int LEFT_JOYSTICK_HORIZONTAL_AXIS   = 0;
constexpr int LEFT_JOYSTICK_VERTICAL_AXIS     = 1;
constexpr int RIGHT_JOYSTICK_HORIZONTAL_AXIS  = 3;
constexpr int RIGHT_JOYSTICK_VERTICAL_AXIS    = 4;
constexpr int LEFT_TRIGGER_AXIS               = 2;
constexpr int RIGHT_TRIGGER_AXIS              = 5;
constexpr int DPAD_HORIZONTAL_AXIS            = 6;
constexpr int DPAD_VERTICAL_AXIS              = 7;

constexpr int SQUARE_BUTTON         = 0;
constexpr int X_BUTTON              = 1;
constexpr int CIRCLE_BUTTON         = 2;
constexpr int TRIANGLE_BUTTON       = 3;
constexpr int LEFT_BUMPER           = 4;
constexpr int RIGHT_BUMPER          = 5;
constexpr int LEFT_TRIGGER          = 6;
constexpr int RIGHT_TRIGGER         = 7;
constexpr int SHARE_BUTTON          = 8;
constexpr int OPTIONS_BUTTON        = 9;
constexpr int LEFT_JOYSTICK_BUTTON  = 10;
constexpr int RIGHT_JOYSTICK_BUTTON = 11;
constexpr int PLAYSTATION_BUTTON    = 12;
constexpr int TOUCHPAD_BUTTON       = 13;

DriveTeleopNode::DriveTeleopNode() : 
  Node("drive_teleop_node")
{
  // Declare parameters
  RCLCPP_DEBUG(get_logger(), "Declaring speed");
  speed_axis_      = this->declare_parameter("axes.left", LEFT_JOYSTICK_VERTICAL_AXIS);
  RCLCPP_DEBUG(get_logger(), "Declaring turn");
  turn_axis_     = this->declare_parameter("axes.right", RIGHT_JOYSTICK_HORIZONTAL_AXIS);
  RCLCPP_DEBUG(get_logger(), "Declaring deadman");
  deadman_switch_ = this->declare_parameter("axes.deadman", RIGHT_TRIGGER_AXIS); // Axis that MUST BE HELD for any movement to occur

  RCLCPP_DEBUG(get_logger(), "Declaring max pwm");
  // this->declare_parameter("max_pwm", 32000);
  // RCLCPP_DEBUG(get_logger(), "Declaring publish");
  // this->declare_parameter("publish_rate", 50); // Hz
  // RCLCPP_DEBUG(get_logger(), "Declaring expo");
  // this->declare_parameter("expo", 0.3); // Coefficient for expo input equation

  // Init pub and sub
  joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
    "/joy", ROS_QUEUE_SIZE,
    std::bind(&DriveTeleopNode::joy_callback, this, std::placeholders::_1)
  );

  drive_pub_ = this->create_publisher<drive_teleop::msg::DriveControlMessage>(DRIVE_OUT_TOPIC, ROS_QUEUE_SIZE);
  
  RCLCPP_INFO(get_logger(), "Drive teleop node started");
}

void DriveTeleopNode::joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg)
{
  // Get max velocities to cap outputs at
  // int max_pwm = this->get_parameter("max_pwm").as_int();
  double max_pwm = 32000.0;

  // Make output message
  auto drive_msg = std::make_unique<drive_teleop::msg::DriveControlMessage>();

  // Check deadman switch (all output 0 unless pressed)
  bool deadman_pressed = (get_axis_value(msg, deadman_switch_) < -0.5);

  drive_msg->header.frame_id = DRIVE_FRAME_ID;
  drive_msg->header.stamp    = this->now();

  double speed = 0.0;
  double turn = 0.0;
  double left_input = 0.0;
  double right_input = 0.0;

  if (deadman_pressed) {
    speed = get_axis_value(msg, speed_axis_);
    turn = -get_axis_value(msg, turn_axis_);

    // Calculate left and right speed from turn
    left_input = speed + turn;
    right_input = speed - turn;

    // Apply deadband
    //TODO

    drive_msg->left_input_pwm   = static_cast<int>(compute_velocity_output(left_input, max_pwm));
    drive_msg->right_input_pwm  = static_cast<int>(compute_velocity_output(right_input, max_pwm));
  }

  RCLCPP_DEBUG(get_logger(), "Drive deadman switch pressed: %d", deadman_pressed);
  RCLCPP_DEBUG(get_logger(), "Drive speed input (-1, 1): %.2f", speed);
  RCLCPP_DEBUG(get_logger(), "Drive turn input (-1, 1): %.2f", turn);
  RCLCPP_DEBUG(get_logger(), "Drive left input (-1, 1): %.2f", left_input);
  RCLCPP_DEBUG(get_logger(), "Drive right input (-1, 1): %.2f", right_input);
  RCLCPP_DEBUG(get_logger(), "Drive left pwm (-32000, 32000): %d", drive_msg->left_input_pwm);
  RCLCPP_DEBUG(get_logger(), "Drive right pwm (-32000, 32000): %d", drive_msg->right_input_pwm);

  drive_pub_->publish(std::move(drive_msg));
}

double DriveTeleopNode::get_button_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index)
{
  // Check index validity
  int length = BUTTON_COUNT;
  if (index < 0 || index >= length) {
    return 0.0;
  }

  // If index is valid:
  return msg->buttons[index];
}

double DriveTeleopNode::get_axis_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index) {
  // Check index validity
  int length = AXIS_COUNT;
  if (index < 0 || index >= length) {
    RCLCPP_WARN(get_logger(), "Axis value ignored! index: %d; axis message length: %d", index, length);
    return 0.0;
  }

  // If index is valid:
  return msg->axes[index];
}

double DriveTeleopNode::compute_velocity_output(double raw_value, double max_velocity) {
  // Don't set in constructor as this may change during execution
  RCLCPP_DEBUG(get_logger(), "Getting expo");
  double expo = 0.3;
  // double expo = this->get_parameter("expo").as_double();

  // Perform input smoothing near 0 using 3rd-degree polynomial equation
  // The higher the value of "expo", the greater the smoothing
  // Note that inputs of -1, 0, and 1 all map to their original values
  double expo_value = (1.0 - expo) * raw_value + expo * (raw_value * raw_value * raw_value);
  
  // Clamp value just in case
  expo_value = std::clamp(expo_value, -1.0, 1.0);

  // Now scale value by max velocity
  // TODO: limit acceleration, add deadband
  double v = expo_value * max_velocity;

  return v;
}

double DriveTeleopNode::apply_deadband(double value, double deadband) {
  if (std::abs(value) < deadband) {
    return 0.0;
  } else {
    return value;
  }
}

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<DriveTeleopNode>());
  rclcpp::shutdown();
  return 0;
}