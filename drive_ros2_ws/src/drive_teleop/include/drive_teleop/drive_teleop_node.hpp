#include <chrono>
#include <memory>

#include <cmath>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "drive_teleop/msg/drive_control_message.hpp"

using namespace std::chrono_literals;

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