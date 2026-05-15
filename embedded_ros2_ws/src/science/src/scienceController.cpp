#include <rclcpp/rclcpp.hpp>
#include <stepper_can/msg/control_message.hpp>
#include <stepper_can/msg/controller_status.hpp>
#include <stepper_node/msg/control_message.hpp>
#include <stepper_node/msg/controller_status.hpp>
#include <stepper_can/srv/axis_state.hpp>
#include <std_srvs/srv/empty.hpp>
#include <servo/msg/control_message.hpp>
#include <odrive_node/msg/control_message.hpp>
#include <chrono>
#include <std_msgs/msg/int32_multi_array.hpp>
#include <std_msgs/msg/bool.hpp>
#include <memory>

using namespace std::chrono_literals;

class StepperController : public rclcpp::Node {
public:
    StepperController() : Node("stepper_controller") {
        // Publisher for control messages
        control_publisher0_ = this->create_publisher<stepper_node::msg::ControlMessage>(
            "/stepper_drill/control_message", 10);
        
        status_subscriber0_ = this->create_subscription<stepper_node::msg::ControllerStatus>(
            "/stepper_drill/controller_status", 10,
            std::bind(&StepperController::status_callback_stepper, this, std::placeholders::_1));


        control_publisher1_ = this->create_publisher<stepper_node::msg::ControlMessage>(
            "/stepper_sensor/control_message", 10);
        
        status_subscriber1_ = this->create_subscription<stepper_node::msg::ControllerStatus>(
            "/stepper_sensor/controller_status", 10,
            std::bind(&StepperController::status_callback_stepper, this, std::placeholders::_1));

        
        servo_publisher_ = this->create_publisher<servo::msg::ControlMessage>( //change the message type
            "/servo/control_message", 10);
        
        odrive_publisher_ = this->create_publisher<odrive::msg::ControlMessage>(
            "/odrive/control_message", 10);
        odrive_status_subscriber_ = this->create_subscription<odrive::msg::ControllerStatus>(
            "/odrive/controller_status", 10,
            std::bind(&StepperController::status_callback_odrive, this, std::placeholders::_1));
        

        command_subscriber_ = this->create_subscription<std_msgs::msg::Int32MultiArray>(
            "science_command", 10, std::bind(&StepperController::command_callback, this, std::placeholders::_1));

        science_status_publisher_ = this->create_publisher<std_msgs::msg::Bool>("science_status", 10);
        // Service clients
        
        RCLCPP_INFO(this->get_logger(), "Stepper controller initialized");
    }

private:

    void status_callback_stepper(const stepper_node::msg::ControllerStatus::SharedPtr msg) {
        if(msg->pos_estimate == 200){ //check if the motor has extended down 10 inches
            auto message = std_msgs::msg::Bool();
            message.data = true;
            science_status_publisher_->publish(message);

        }
    }
    void status_callback_odrive(const odrive::msg::ControllerStatus::SharedPtr msg) {
        if (msg->vel_estimate == 100){ //full speed
            auto message = std_msgs::msg::Bool();
            message.data = true;
            science_status_publisher_->publish(message);

        }
    }

    void command_callback(const std_msgs::msg::Int32MultiArray::SharedPtr msg) {

        int motorNum = msg->data[0]; 
        int value_command = msg->data[1];

        if (motorNum == -2){
            auto control_msg = odrive::msg::ControlMessage();
            control_msg.control_mode = 2;  // velocity control
            control_msg.input_vel = value_command;  // Velocity setpoint
            odrive_publisher_->publish(control_msg);
            return;
        }

        if (motorNum == 0){
            auto control_msg = stepper_node::msg::ControlMessage();
            control_msg.control_mode = 3;  // Position control
            control_msg.input_mode = 0;    // Default input mode
            control_msg.input_vel = value_command;  // Position setpoint
            control_msg.input_torque = 0;  // Feedforward torque
            control_publisher0_->publish(control_msg);

        }
        else if (motorNum == 1){
            auto control_msg = stepper_node::msg::ControlMessage();
            control_msg.control_mode = 3;  // Position control
            control_msg.input_mode = 0;    // Default input mode
            control_msg.input_vel = value_command;  // Position setpoint
            control_msg.input_torque = 0;  // Feedforward torque
            control_publisher1_->publish(control_msg);
        }

        else if (motorNum == 2){
            auto control_msg = servo::msg::ControlMessage();
            control_msg.control_mode = 2;  // Position control
            control_msg.input_pos_deg = value_command;  // Position setpoint in degrees
            servo_publisher_->publish(control_msg);
        }
        
        else if (motorNum == 3){
            auto control_msg = servo::msg::ControlMessage();
            control_msg.control_mode = 2;  // Velocity control
            control_msg.input_vel_deg = value_command;  // Velocity setpoint in degrees/s
            servo_publisher_->publish(control_msg);
        }
        
    }

    // Method to set axis state (call this to enable/disable motor)
    void set_axis_state(uint32_t state) {
        if (!axis_state_client_->wait_for_service(1s)) {
            RCLCPP_ERROR(this->get_logger(), "Axis state service not available");
            return;
        }
        
        auto request = std::make_shared<stepper_can::srv::AxisState::Request>();
        request->axis_requested_state = state;
        
        auto future = axis_state_client_->async_send_request(request);
        
        // In a real application, you'd handle the future properly
        RCLCPP_INFO(this->get_logger(), "Requested axis state: %d", state);
    }

    // Method to clear errors
    void clear_errors() {
        if (!clear_errors_client_->wait_for_service(1s)) {
            RCLCPP_ERROR(this->get_logger(), "Clear errors service not available");
            return;
        }
        
        auto request = std::make_shared<std_srvs::srv::Empty::Request>();
        auto future = clear_errors_client_->async_send_request(request);
        
        RCLCPP_INFO(this->get_logger(), "Requested error clearing");
    }

    rclcpp::Publisher<stepper_node::msg::ControlMessage>::SharedPtr control_publisher0_;
    rclcpp::Publisher<stepper_node::msg::ControlMessage>::SharedPtr control_publisher1_;
    rclcpp::Subscription<stepper_node::msg::ControllerStatus>::SharedPtr status_subscriber0_;    
    rclcpp::Subscription<stepper_node::msg::ControllerStatus>::SharedPtr status_subscriber1_;    
    rclcpp::Publisher<servo::msg::ControlMessage>::SharedPtr servo_publisher_;
    rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr science_status_publisher_;
    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr command_subscriber_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    
    auto controller = std::make_shared<StepperController>();
    
    // Enable the motor (set to closed loop control)
    // You'll need to call this once to enable the motor
    // controller->set_axis_state(8);  // AXIS_STATE_CLOSED_LOOP_CONTROL
    
    rclcpp::spin(controller);
    rclcpp::shutdown();
    return 0;
}