#include "servo_node/servo_node.hpp"
// #include "epoll_event_loop.hpp"
#include <thread>

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    // EpollEventLoop event_loop;
    auto servo_node = std::make_shared<ServoNode>("ServoNode");

    // if (!servo_node->init(&event_loop)) return -1;
    if (!servo_node->init()) return -1;

    // std::thread can_event_loop([&event_loop]() { event_loop.run_until_empty(); });
    rclcpp::spin(servo_node);
    servo_node->deinit();
    rclcpp::shutdown();
    return 0;
}
