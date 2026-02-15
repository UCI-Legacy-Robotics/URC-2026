#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"

using namespace std::chrono_literals;

class MockGpsNode : public rclcpp::Node
{
public:
  MockGpsNode() : Node("mock_gps_node")
  {
    publisher_ = this->create_publisher<sensor_msgs::msg::NavSatFix>("/fix", 10);
    timer_ = this->create_wall_timer(
      1000ms, std::bind(&MockGpsNode::timer_callback, this));
      
    RCLCPP_INFO(this->get_logger(), "Dynamic Mock GPS Started. Simulating movement...");
  }

private:
  // Set our starting location
  double current_lat_ = 33.7455;
  double current_lon_ = -117.8677;
  double current_alt_ = 35.0;

  void timer_callback()
  {
    auto msg = sensor_msgs::msg::NavSatFix();
    msg.header.stamp = this->now();
    msg.header.frame_id = "gps_link"; 

    // Simulate movement: Add a tiny offset (~5 meters) every second
    current_lat_ += 0.00005;
    current_lon_ += 0.00005;
    // Simulate slight altitude variations
    current_alt_ += 0.1; 

    msg.latitude = current_lat_;
    msg.longitude = current_lon_;
    msg.altitude = current_alt_;

    msg.status.status = sensor_msgs::msg::NavSatStatus::STATUS_FIX;
    msg.status.service = sensor_msgs::msg::NavSatStatus::SERVICE_GPS;

    RCLCPP_INFO(this->get_logger(), "Moving -> Lat: %.5f, Lon: %.5f", msg.latitude, msg.longitude);
    
    publisher_->publish(msg);
  }
  
  rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MockGpsNode>());
  rclcpp::shutdown();
  return 0;
}
