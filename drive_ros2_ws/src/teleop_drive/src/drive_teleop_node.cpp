#include <chrono>
#include <memory>

#include <cmath>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>

using namespace std::chrono_literals;

// Define constants
constexpr int AXIS_COUNT = 8;
constexpr int BUTTON_COUNT = 14;
constexpr size_t ROS_QUEUE_SIZE = 10;

const std::string DRIVE_OUT_TOPIC = "/drive_teleop_node/command";

constexpr int MAX_DRIVE_PWM = 32767;

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
    DriveTeleopNode() : 
      Node("drive_teleop_node")
    {
      // Declare parameters
      left_axis_      = this->declare_parameter("axes.left", LEFT_JOYSTICK_VERTICAL_AXIS);
      right_axis_     = this->declare_parameter("axes.right", RIGHT_JOYSTICK_VERTICAL_AXIS);
      deadman_switch_ = this->declare_parameter("axes.deadman", RIGHT_TRIGGER_AXIS); // Axis that MUST BE HELD for any movement to occur

      this->declare_parameter("max_pwm", MAX_DRIVE_PWM);
      this->declare_parameter("publish_rate", 50); // Hz
      this->declare_parameter("expo", 0.3); // Coefficient for expo input equation

      // Init pub and sub
      joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
        "/joy", ROS_QUEUE_SIZE,
        std::bind(&ArmTeleop::joy_callback, this, std::placeholders::_1)
      );

      drive_pub_ = this->create_publisher<teleop_drive::msg::DriveControlMessage>(DRIVE_OUT_TOPIC, ROS_QUEUE_SIZE);
      
      RCLCPP_INFO(get_logger(), "Drive teleop node started");
    }

  private:
    void joy_callback(const sensor_msgs::msg::Joy::SharedPtr msg) {
      // Get max velocities to cap outputs at
      int max_pwm = this->get_parameter("max_pwm").as_double();

      // Make output message
      auto msg = std::make_unique<teleop_drive::msg::Drive;

      // Check deadman switch (all output 0 unless pressed)
      bool deadman_pressed = (get_axis_value(msg, deadman_switch_) < -0.5);

      if (deadman_pressed) {

      }
    }

    void publish_cartesian(
      const sensor_msgs::msg::Joy::SharedPtr msg,
      double max_linear_vel,
      double max_angular_vel,
      bool deadman_pressed,
      bool mode_toggle_button_pressed
    ) {
      auto cartesian_msg = std::make_unique<geometry_msgs::msg::TwistStamped>();

      // Axes come from parameters
      // First get the value from each axis
      double x      = get_axis_value(msg, x_axis_);
      double y      = -get_axis_value(msg, y_axis_);
      double z      = get_axis_value(msg, z_axis_);

      // These come from dpad
      double roll   = -get_axis_value(msg, roll_axis_);
      // RCLCPP_INFO(get_logger(), "Joystick roll: %.2f", roll);
      double pitch  = get_axis_value(msg, pitch_axis_);
      // RCLCPP_INFO(get_logger(), "Joystick pitch: %.2f", pitch);

      // These always come from buttons, set default first
      constexpr double YAW_SPEED = 1.0; // rad/s
      double yaw = 0.0;

      // Set yaw
      if (get_button_value(msg, yaw_negative_button_) == 1) {
        yaw = -YAW_SPEED;
      } else if (get_button_value(msg, yaw_positive_button_) == 1) {
        yaw = YAW_SPEED;
      }

      // Set the frame to twist relative to and the timestamp
      // In this case it's our end effector
      cartesian_msg->header.frame_id = END_EFFECTOR_FRAME_ID;
      cartesian_msg->header.stamp    = this->now();

      if (deadman_pressed) {
        cartesian_msg->twist.linear.x  = compute_velocity_output(x, max_linear_vel);
        cartesian_msg->twist.linear.y  = compute_velocity_output(y, max_linear_vel);
        cartesian_msg->twist.linear.z  = compute_velocity_output(z, max_linear_vel);
        cartesian_msg->twist.angular.x = compute_velocity_output(roll, max_angular_vel);
        cartesian_msg->twist.angular.y = compute_velocity_output(pitch, max_angular_vel);
        cartesian_msg->twist.angular.z = compute_velocity_output(yaw, max_angular_vel);

        // Apply deadbands
        cartesian_msg->twist.linear.x  = apply_deadband(cartesian_msg->twist.linear.x, CARTESIAN_LINEAR_DEADBAND);
        cartesian_msg->twist.linear.y  = apply_deadband(cartesian_msg->twist.linear.y, CARTESIAN_LINEAR_DEADBAND);
        cartesian_msg->twist.linear.z  = apply_deadband(cartesian_msg->twist.linear.z, CARTESIAN_LINEAR_DEADBAND);
        cartesian_msg->twist.angular.x  = apply_deadband(cartesian_msg->twist.angular.x, JOINT_VELOCITY_DEADBAND);
        cartesian_msg->twist.angular.y  = apply_deadband(cartesian_msg->twist.angular.y, JOINT_VELOCITY_DEADBAND);
        cartesian_msg->twist.angular.z  = apply_deadband(cartesian_msg->twist.angular.z, JOINT_VELOCITY_DEADBAND);

        update_control_mode(msg, mode_toggle_button_pressed);
      }

      RCLCPP_DEBUG(get_logger(), "Arm control mode: %s", cartesian_mode_ ? "Cartesian" : "Joint");
      RCLCPP_DEBUG(get_logger(), "Arm deadman switch pressed: %d", deadman_pressed);
      RCLCPP_DEBUG(get_logger(), "Arm x input: %.2f; x output (m/s): %.2f", x, cartesian_msg->twist.linear.x);
      RCLCPP_DEBUG(get_logger(), "Arm y input: %.2f; y output (m/s): %.2f", y, cartesian_msg->twist.linear.y);
      RCLCPP_DEBUG(get_logger(), "Arm z input: %.2f; z output (m/s): %.2f", z, cartesian_msg->twist.linear.z);
      RCLCPP_DEBUG(get_logger(), "Arm roll input: %.2f; roll output (rad/s): %.2f", roll, cartesian_msg->twist.angular.x);
      RCLCPP_DEBUG(get_logger(), "Arm pitch input: %.2f; pitch output (rad/s): %.2f", pitch, cartesian_msg->twist.angular.y);
      RCLCPP_DEBUG(get_logger(), "Arm yaw input: %.2f; yaw output (rad/s): %.2f", yaw, cartesian_msg->twist.angular.z);

      teleop_cartesian_pub_->publish(std::move(cartesian_msg));
    }

    void publish_joint(
      const sensor_msgs::msg::Joy::SharedPtr msg,
      double max_angular_vel,
      bool deadman_pressed,
      bool mode_toggle_button_pressed
    ) {
      auto joint_msg = std::make_unique<control_msgs::msg::JointJog>();

      // Load in joint names
      joint_msg->joint_names.push_back("base");
      joint_msg->joint_names.push_back("shoulder");
      joint_msg->joint_names.push_back("elbow");
      joint_msg->joint_names.push_back("wrist_pitch");
      joint_msg->joint_names.push_back("wrist_roll");

      // Axes come from parameters
      // First get the value from each axis
      double base     = get_axis_value(msg, x_axis_);
      double shoulder = get_axis_value(msg, y_axis_);
      double elbow    = get_axis_value(msg, z_axis_);

      // These come from dpad
      double wrist_pitch  = -get_axis_value(msg, roll_axis_);
      double wrist_roll   = -get_axis_value(msg, pitch_axis_);

      // Set the frame to jog joints relative to and the timestamp
      // In this case it's the base since these are joint velocities
      joint_msg->header.frame_id = BASE_FRAME_ID;
      joint_msg->header.stamp    = this->now();

      if (deadman_pressed) {
        // Add respective joint velocities, angular if angular joint linear if linear joint
        joint_msg->velocities.push_back(compute_velocity_output(base, max_angular_vel));
        joint_msg->velocities.push_back(compute_velocity_output(shoulder, max_angular_vel));
        joint_msg->velocities.push_back(compute_velocity_output(elbow, max_angular_vel));
        joint_msg->velocities.push_back(compute_velocity_output(wrist_pitch, max_angular_vel));
        joint_msg->velocities.push_back(compute_velocity_output(wrist_roll, max_angular_vel));

        // Apply deadbands
        for (size_t i = 0; i < joint_msg->joint_names.size(); i++) {
          joint_msg->velocities[i] = apply_deadband(joint_msg->velocities[i], JOINT_VELOCITY_DEADBAND);
        }

        update_control_mode(msg, mode_toggle_button_pressed);
      } else {
        for (size_t i = 0; i < joint_msg->joint_names.size(); i++) {
          joint_msg->velocities.push_back(0.0);
        }
      }

      RCLCPP_DEBUG(get_logger(), "Arm control mode: %s", cartesian_mode_ ? "Cartesian" : "Joint");
      RCLCPP_DEBUG(get_logger(), "Arm deadman switch pressed: %d", deadman_pressed);
      RCLCPP_DEBUG(get_logger(), "Arm base input: %.2f; base output (rad/s): %.2f", base, joint_msg->velocities[0]);
      RCLCPP_DEBUG(get_logger(), "Arm shoulder input: %.2f; shoulder output (rad/s): %.2f", shoulder, joint_msg->velocities[1]);
      RCLCPP_DEBUG(get_logger(), "Arm elbow input: %.2f; elbow output (rad/s): %.2f", elbow, joint_msg->velocities[2]);
      RCLCPP_DEBUG(get_logger(), "Arm wrist pitch input: %.2f; wrist pitch output (rad/s): %.2f", wrist_pitch, joint_msg->velocities[3]);
      RCLCPP_DEBUG(get_logger(), "Arm wrist roll input: %.2f; wrist roll output (rad/s): %.2f", wrist_roll, joint_msg->velocities[4]);

      teleop_joint_pub_->publish(std::move(joint_msg));
    }

    void publish_gripper(
      const sensor_msgs::msg::Joy::SharedPtr msg,
      bool deadman_pressed,
      double time_diff_seconds
    ) {
      // Gripper message is published in both control modes
      // Offers direct control of solenoid linear actuator and gripper actuation
      auto gripper_msg = std::make_unique<trajectory_msgs::msg::JointTrajectory>();
      trajectory_msgs::msg::JointTrajectoryPoint point;

      // Load in joint names
      gripper_msg->joint_names.push_back("solenoid");
      gripper_msg->joint_names.push_back("gripper");

      constexpr double SOLENOID_SPEED = -0.05; // m/s
      constexpr double GRIPPER_SPEED = 0.5; // rad/s

      double solenoid_linear_actuator_speed = 0.0;
      double gripper_actuation_speed        = 0.0;

      // Set solenoid linear actuator speed
      if (get_button_value(msg, solenoid_left_button_) == 1) {
        solenoid_linear_actuator_speed = -SOLENOID_SPEED;
      } else if (get_button_value(msg, solenoid_right_button_) == 1) {
        solenoid_linear_actuator_speed = SOLENOID_SPEED;
      }

      // Set gripper actuation speed
      if (get_button_value(msg, gripper_open_button_) == 1) {
        gripper_actuation_speed = -GRIPPER_SPEED;
      } else if (get_button_value(msg, gripper_close_button_) == 1) {
        gripper_actuation_speed = GRIPPER_SPEED;
      }

      // Set the frame to jog joints relative to and the timestamp
      // In this case it's the base since these are joint velocities
      gripper_msg->header.frame_id = BASE_FRAME_ID;
      gripper_msg->header.stamp    = this->now();

      // Integrate velocity
      solenoid_position_ += solenoid_linear_actuator_speed * time_diff_seconds;
      gripper_position_ += gripper_actuation_speed * time_diff_seconds;

      // Clamp positions within limits
      solenoid_position_ = std::clamp(solenoid_position_, SOLENOID_MIN_LIMIT, SOLENOID_MAX_LIMIT);
      gripper_position_ = std::clamp(gripper_position_, GRIPPER_MIN_LIMIT, GRIPPER_MAX_LIMIT);

      point.positions.push_back(solenoid_position_);
      point.positions.push_back(gripper_position_);

      if (deadman_pressed) {
        // Add respective joint velocities, angular if angular joint linear if linear joint
        point.velocities.push_back(solenoid_linear_actuator_speed);
        point.velocities.push_back(gripper_actuation_speed);
      } else {
        for (size_t i = 0; i < gripper_msg->joint_names.size(); i++) {
          point.velocities.push_back(0.0);
        }
      }

      point.time_from_start = rclcpp::Duration::from_seconds(0.1);
      gripper_msg->points.push_back(point);

      RCLCPP_DEBUG(get_logger(), "Arm solenoid actuator input: %.2f", solenoid_linear_actuator_speed);
      RCLCPP_DEBUG(get_logger(), "Arm gripper input: %.2f", gripper_actuation_speed);

      gripper_pub_->publish(std::move(gripper_msg));
    }

    void update_control_mode(const sensor_msgs::msg::Joy::SharedPtr msg, bool mode_toggle_button_pressed) {
      // If rising edge on toggle button and deadman pressed and axes neutral,
      // toggle cartesian vs. joint mode on toggle button press
      double x      = get_axis_value(msg, x_axis_);
      double y      = -get_axis_value(msg, y_axis_);
      double z      = get_axis_value(msg, z_axis_);
      bool axes_neutral = 
        std::abs(x) < 0.1 &&
        std::abs(y) < 0.1 &&
        std::abs(z) < 0.1;

      if (mode_toggle_button_pressed && !mode_toggle_button_previously_pressed_
          && axes_neutral) {
        cartesian_mode_ = !cartesian_mode_;
        RCLCPP_INFO(get_logger(),
          "Mode switched to: %s",
          cartesian_mode_ ? "Cartesian" : "Joint");
      }

      // Save state for next callback
      mode_toggle_button_previously_pressed_ = mode_toggle_button_pressed;
    }

    double get_button_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index) {
      // Check index validity
      int length = BUTTON_COUNT;
      if (index < 0 || index >= length) {
        return 0.0;
      }

      // If index is valid:
      return msg->buttons[index];
    }

    double get_axis_value(const sensor_msgs::msg::Joy::SharedPtr &msg, int index) {
      // Check index validity
      int length = AXIS_COUNT;
      if (index < 0 || index >= length) {
        RCLCPP_WARN(get_logger(), "Axis value ignored! index: %d; axis message length: %d", index, length);
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

    double apply_deadband(double value, double deadband) {
      if (std::abs(value) < deadband) {
        return 0.0;
      } else {
        return value;
      }
    }

    // States
    bool first_callback_;
    rclcpp::Time last_callback_time_;
    double solenoid_position_;
    double gripper_position_;

    // ROS interfaces
    rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
    rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr teleop_cartesian_pub_;
    rclcpp::Publisher<control_msgs::msg::JointJog>::SharedPtr teleop_joint_pub_; // Joint-space commands
    rclcpp::Publisher<trajectory_msgs::msg::JointTrajectory>::SharedPtr gripper_pub_; // Commands just for gripper, which are used both in cartesian and joint modes

    // Parameters
    int x_axis_, y_axis_, z_axis_;
    int roll_axis_, pitch_axis_;
    int yaw_negative_button_, yaw_positive_button_;
    int solenoid_left_button_, solenoid_right_button_;
    int gripper_open_button_, gripper_close_button_;
    int deadman_switch_;
    int mode_toggle_button_;

    bool cartesian_mode_ = true;
    bool mode_toggle_button_previously_pressed_ = false;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ArmTeleop>());
  rclcpp::shutdown();
  return 0;
}