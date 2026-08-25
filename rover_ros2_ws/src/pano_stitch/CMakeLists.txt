cmake_minimum_required(VERSION 3.10)
project(pano_stitch_ros2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(OpenCV REQUIRED)

add_executable(pano_stitch_node
  src/pano_stitch_node.cpp
  src/stitcher.cpp
)

target_include_directories(pano_stitch_node PRIVATE include)

ament_target_dependencies(pano_stitch_node
  rclcpp
  cv_bridge
  image_transport
  sensor_msgs
  std_msgs
  std_srvs
)

target_link_libraries(pano_stitch_node ${OpenCV_LIBS})

install(TARGETS pano_stitch_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
