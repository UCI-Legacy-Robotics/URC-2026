#include <chrono>
#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int32_multi_array.hpp>
#include <std_msgs/msg/bool.hpp>
#include "npk_sensor/srv/get_soil_data.hpp"
using GetSoilData = npk_sensor::srv::GetSoilData;


using namespace std::chrono_literals;


class ScienceLogic : public rclcpp::Node {

public:
    ScienceLogic() : Node("science_logic") {
        RCLCPP_INFO(this->get_logger(), "Science logic node initialized");


        client_ = this->create_client<GetSoilData>("get_soil_data");


        commandPublisher_ = this->create_publisher<std_msgs::msg::Int32MultiArray>("science_command", 10);

        commandSubscriber_ = this->create_subscription<std_msgs::msg::Bool>(
            "science_status", 10, std::bind(&ScienceLogic::status_callback, this, std::placeholders::_1));

        roverPositionSubscriber_ = this->create_subscription<std_msgs::msg::Bool>(
            "rover_position", 10, std::bind(&ScienceLogic::position_callback, this, std::placeholders::_1)); 

        timer_ = this->create_wall_timer(500ms, std::bind(&ScienceLogic::timer_callback, this));
        
        

    }
private:
    bool flag = false;
    bool moved = false;
    int states = 0;
    

    void requestSoilData(){
        auto request = std::make_shared<GetSoilData::Request>();

        while (!client_->wait_for_service(1s)) {
            RCLCPP_WARN(this->get_logger(), "Waiting for get_soil_data service...");
        }

        auto future = client_->async_send_request(request, std::bind(&ScienceLogic::handle_response, this, std::placeholders::_1));
        // In a real application, you'd want to handle the future properly
    }

    void handle_response(rclcpp::Client<GetSoilData>::SharedFuture future) {
        auto response = future.get();
        if (response !=nullptr && states == 4){
            flag = true;
        }
    }

     
    void status_callback(const std_msgs::msg::Bool::SharedPtr msg) {
        if (msg->data == true){
            flag = true;
        }
    }
    void position_callback(const std_msgs::msg::Bool::SharedPtr msg) {
        if (msg->data == true){
            moved = true;
        }
    }
    void timer_callback() {
        auto message = std_msgs::msg::Int32MultiArray();
        if (states == 0){
            message.data = {-2.0, 1.0}; // set the drill speed
            if (flag == true){
                flag = false;
                states++;
            }
        }
        if (states == 1){
            message.data = {0, 1.0}; // drill motor go down
            if (flag == true){
                flag = false;
                states++;
            }
        }
        else if (states == 2){

            message.data = {0, 1.0}; // drill motor go up
            if (flag == true){  //flag should only turn true after rover moves to the next whole
                flag = false;
                states++;
            }
        }
        
        else if (states == 3){
            message.data = {1, 1.0}; // sensor motor
            if (flag == true){
                flag = false;
                states ++;
            }
        }

        else if (states == 4){
            requestSoilData();
            message.data = {-1,0}; // request soil data, wait for response to move on
            if (flag == true){
                flag = false;
                states++;
            }
        }
        else if (states == 5){
            message.data = {2, 1.0}; //move servor
            if (flag == true){
                flag = false;
                states++ ;
            }
        }
        else if (states == 6){
            message.data = {1, 1.0}; //move sensor motor up
            if (flag == true){
                flag = false;
                states++;
            }
        }
        else if (states == 7){
            message.data = {2, 1.0}; //move servor up
            if (flag == true){
                flag = false;
                states++;
            }
        }
        else
        {
            message.data = {3, 1.0}; // move pump
        }

        if(message.data[0] != -1) // don't publish if just requesting soil data
            commandPublisher_->publish(message);

        RCLCPP_INFO(this->get_logger(), "Current state: %d", states);
    }

    rclcpp::Publisher<std_msgs::msg::Int32MultiArray>::SharedPtr commandPublisher_;
    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr commandSubscriber_;
    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr roverPositionSubscriber_;
    rclcpp::Client<GetSoilData>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;

};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ScienceLogic>());
    rclcpp::shutdown();
    return 0;
}2