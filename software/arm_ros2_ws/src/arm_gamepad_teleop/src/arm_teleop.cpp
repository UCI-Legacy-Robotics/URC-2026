#include <chrono>
#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <sensor_msgs/msg/joy.hpp>

using namespace std::chrono_literals;

class ArmTeleop : public rclcpp::Node {
  public:
    ArmTeleop() : Node("arm_teleop") {
      // Declare parameters
      x_axis_     = this->declare_parameter("axes.x", 0);
      y_axis_     = this->declare_parameter("axes.y", 1);
      z_axis_     = this->declare_parameter("axes.z", 3);
      roll_axis_  = this->declare_parameter("axes.roll", 4);
      pitch_axis_ = this->declare_parameter("axes.pitch", 5);
      yaw_axis_   = this->declare_parameter("axes.yaw", 2);

      this->declare_parameter("max_linear_velocity", 0.3);   // Meters per second
      this->declare_parameter("max_angular_velocity", 0.5);  // Radians per second
      this->declare_parameter("publish_rate", 50);           // Hz
      this->declare_parameter("expo", 0.3);                  // Coefficient for expo input equation

      // Init pub and sub
      joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
        "/joy", 10,
        std::bind(&ArmTeleop::joy_callback, this, std::placeholders::_1)
      );

      teleop_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/arm/velocities", 10);
      
      RCLCPP_INFO(get_logger(), "Arm teleop node started");
    }

  private:
    void joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg) {
      geometry_msgs::msg::Twist out_msg;

      // Axes come from parameters
      // First get the value from each axis
      double x      = get_axis_value(msg, x_axis_);
      double y      = get_axis_value(msg, y_axis_);
      double z      = get_axis_value(msg, z_axis_);
      double roll   = get_axis_value(msg, roll_axis_);
      double pitch  = get_axis_value(msg, pitch_axis_);
      double yaw    = get_axis_value(msg, yaw_axis_);

      // Now convert to velocities using the current max velocities
      double max_linear_vel = this->get_parameter("max_linear_velocity").as_double();
      double max_angular_vel = this->get_parameter("max_angular_velocity").as_double();

      out_msg.linear.x  = compute_velocity_output(x, max_linear_vel);
      out_msg.linear.y  = compute_velocity_output(y, max_linear_vel);
      out_msg.linear.z  = compute_velocity_output(z, max_linear_vel);
      out_msg.angular.x = compute_velocity_output(roll, max_angular_vel);
      out_msg.angular.y = compute_velocity_output(pitch, max_angular_vel);
      out_msg.angular.z = compute_velocity_output(yaw, max_angular_vel);

      teleop_pub_->publish(out_msg);
    }

    double get_axis_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index) {
      // Check index validity
      int length = sizeof(msg->axes) / sizeof(msg->axes[0]);
      if (index < 0 || index >= length) {
        return 0.0;
      }

      // If index is valid:
      return msg->axes[index];
    }

    double compute_velocity_output(double raw_value, double max_velocity) {
      // Don't set in constructor as this may change during execution
      double expo = this->get_parameter("expo").as_double();

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

    // ROS interfaces
    rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr teleop_pub_;

    // Parameters
    int x_axis_, y_axis_, z_axis_;
    int roll_axis_, pitch_axis_, yaw_axis_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmTeleop>());
  rclcpp::shutdown();
  return 0;
}