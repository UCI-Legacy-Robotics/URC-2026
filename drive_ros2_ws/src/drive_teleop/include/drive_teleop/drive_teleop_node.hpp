#include <chrono>
#include <memory>

#include <cmath>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "drive_teleop/msg/drive_control_message.hpp"

using namespace std::chrono_literals;

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
constexpr int RIGHT_JOYSTICK_HORIZONTAL_AXIS  = 2;
constexpr int RIGHT_JOYSTICK_VERTICAL_AXIS    = 5;
constexpr int LEFT_TRIGGER_AXIS               = 3;
constexpr int RIGHT_TRIGGER_AXIS              = 4;
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

class DriveTeleopNode : public rclcpp::Node {
  public:
    DriveTeleopNode();

  private:
    void joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg);

    double get_button_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index);

    double get_axis_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index);

    double compute_velocity_output(double raw_value, double max_velocity);

    double apply_deadband(double value, double deadband);

    // ROS interfaces
    rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
    rclcpp::Publisher<drive_teleop::msg::DriveControlMessage>::SharedPtr drive_pub_;

    // Parameters
    int speed_axis_, turn_axis_;
    int deadman_switch_;
};