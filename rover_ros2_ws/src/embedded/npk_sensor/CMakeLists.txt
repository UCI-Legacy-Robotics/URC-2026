cmake_minimum_required(VERSION 3.8)
project(npk_sensor)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GetSoilData.srv"
)

add_executable(npk_node src/npk_sensor_node.cpp)
ament_target_dependencies(npk_node rclcpp)

rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(npk_node "${cpp_typesupport_target}")

install(TARGETS
  npk_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
