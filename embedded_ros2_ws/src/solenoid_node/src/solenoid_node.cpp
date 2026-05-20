#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/bool.hpp"
#include <gpiod.h>

#define GPIO_CHIP "gpiochip0"
#define GPIO_PIN  17

class SolenoidNode : public rclcpp::Node {
public:
    SolenoidNode() : Node("solenoid_node") {
        chip_ = gpiod_chip_open_by_name(GPIO_CHIP);
        if (!chip_) {
            RCLCPP_WARN(this->get_logger(), "GPIO chip not available, running in log-only mode");
        } else {
            line_ = gpiod_chip_get_line(chip_, GPIO_PIN);
            if (!line_) {
                RCLCPP_WARN(this->get_logger(), "Failed to get GPIO line, running in log-only mode");
            } else if (gpiod_line_request_output(line_, "solenoid_node", 0) < 0) {
                RCLCPP_WARN(this->get_logger(), "Failed to request GPIO output, running in log-only mode");
                line_ = nullptr;
            }
        }

        sub_ = this->create_subscription<std_msgs::msg::Bool>(
            "/solenoid/cmd", 10,
            std::bind(&SolenoidNode::cmd_callback, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "Solenoid node ready on GPIO pin %d", GPIO_PIN);
    }

    ~SolenoidNode() {
        if (line_) {
            gpiod_line_set_value(line_, 0);
            gpiod_line_release(line_);
        }
        if (chip_) {
            gpiod_chip_close(chip_);
        }
    }

private:
    void cmd_callback(const std_msgs::msg::Bool::SharedPtr msg) {
        if (line_) {
            int val = msg->data ? 1 : 0;
            gpiod_line_set_value(line_, val);
        }
        RCLCPP_INFO(this->get_logger(), msg->data ? "Extending" : "Retracting");
    }

    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr sub_;
    gpiod_chip *chip_ = nullptr;
    gpiod_line *line_ = nullptr;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SolenoidNode>());
    rclcpp::shutdown();
    return 0;
}
