cmake_minimum_required(VERSION 3.8)
project(solenoid_node)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(solenoid_node src/solenoid_node.cpp)
ament_target_dependencies(solenoid_node rclcpp std_msgs)
target_link_libraries(solenoid_node gpiod)

install(TARGETS solenoid_node DESTINATION lib/${PROJECT_NAME})

ament_package()
