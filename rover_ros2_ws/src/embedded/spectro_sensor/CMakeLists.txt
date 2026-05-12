cmake_minimum_required(VERSION 3.8)
project(spectro_sensor)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GetSpectroData.srv"
)

add_executable(spectro_node src/spectro_node.cpp)
ament_target_dependencies(spectro_node rclcpp)

rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(spectro_node "${cpp_typesupport_target}")

install(TARGETS
  spectro_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
