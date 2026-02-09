cmake_minimum_required(VERSION 3.8)
project(cubemars_can)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ControlMessage.msg"
  "msg/ControllerStatus.msg"
)
ament_export_dependencies(rosidl_default_runtime)

include_directories(include)
include_directories(../can_base/include)

add_executable(cubemars_can_node 
  ../can_base/src/epoll_event_loop.cpp
  ../can_base/src/socket_can.cpp
  src/cubemars_can_node.cpp
  src/main.cpp
  include/cubemars_can_node.hpp)

ament_target_dependencies(cubemars_can_node
  rclcpp
)

target_compile_features(cubemars_can_node PRIVATE cxx_std_20)

install(
  TARGETS cubemars_can_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(cubemars_can_node "${cpp_typesupport_target}")

ament_package()
