#include <chrono>
#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>
#include <sensor_msgs/msg/joy.hpp>

using namespace std::chrono_literals;

class ArmTeleop : public rclcpp::Node {
  public:
    ArmTeleop() : Node("arm_teleop") {
      // Declare parameters
      x_axis_     = this->declare_parameter("axes.x", 0);
      y_axis_     = this->declare_parameter("axes.y", 1);
      z_axis_     = this->declare_parameter("axes.z", 5);
      roll_axis_  = this->declare_parameter("axes.roll", 3);
      pitch_axis_ = this->declare_parameter("axes.pitch", 4);
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

      teleop_pub_ = this->create_publisher<geometry_msgs::msg::TwistStamped>("/arm_teleop/delta_twist_cmds", 10);
      
      RCLCPP_INFO(get_logger(), "Arm teleop node started");
    }

  private:
    void joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg) {
      geometry_msgs::msg::TwistStamped out_msg;

      // Axes come from parameters
      // First get the value from each axis
      double x      = get_axis_value(msg, x_axis_);
      double y      = -get_axis_value(msg, y_axis_);
      double z      = get_axis_value(msg, z_axis_);
      double roll   = get_axis_value(msg, roll_axis_);
      double pitch  = get_axis_value(msg, pitch_axis_);
      double yaw    = get_axis_value(msg, yaw_axis_);

      // Normalize triggers to be 0 at resting instead of 1
      // Only for axes that use triggers (3 and 4 for PS4)
      roll = normalize_trigger_value(roll);
      pitch = normalize_trigger_value(pitch);
      
      // Now convert to velocities using the current max velocities
      double max_linear_vel = this->get_parameter("max_linear_velocity").as_double();
      double max_angular_vel = this->get_parameter("max_angular_velocity").as_double();

      // Set the frame to twist relative to and the timestamp
      // In this case it's our end effector
      out_msg.header.frame_id = "wrist_roll_link";
      out_msg.header.stamp    = this->now();

      out_msg.twist.linear.x  = compute_velocity_output(x, max_linear_vel);
      out_msg.twist.linear.y  = compute_velocity_output(y, max_linear_vel);
      out_msg.twist.linear.z  = compute_velocity_output(z, max_linear_vel);
      out_msg.twist.angular.x = compute_velocity_output(roll, max_angular_vel);
      out_msg.twist.angular.y = compute_velocity_output(pitch, max_angular_vel);
      out_msg.twist.angular.z = compute_velocity_output(yaw, max_angular_vel);

      RCLCPP_DEBUG(get_logger(), "Arm x input: %.2f; x output (m/s): %.2f", x, out_msg.twist.linear.x);
      RCLCPP_DEBUG(get_logger(), "Arm y input: %.2f; y output (m/s): %.2f", y, out_msg.twist.linear.y);
      RCLCPP_DEBUG(get_logger(), "Arm z input: %.2f; z output (m/s): %.2f", z, out_msg.twist.linear.z);
      RCLCPP_DEBUG(get_logger(), "Arm roll input: %.2f; roll output (rad/s): %.2f", roll, out_msg.twist.angular.x);
      RCLCPP_DEBUG(get_logger(), "Arm pitch input: %.2f; pitch output (rad/s): %.2f", pitch, out_msg.twist.angular.y);
      RCLCPP_DEBUG(get_logger(), "Arm yaw input: %.2f; yaw output (rad/s): %.2f", yaw, out_msg.twist.angular.z);
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

    double normalize_trigger_value(double value) {
      // By default, triggers are at value = 1, 50% = 0, 100% = -1
      // We are mapping to: default 0, 50% = 0.5, 100% = 1.0
      //TODO change this to use dpad and other buttons instead of axes if necessary
      // Or use a directional toggle
      return (1.0 - value) / 2.0;
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
    rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr teleop_pub_;

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