cmake_minimum_required(VERSION 3.8)
project(pano_stitch_ros2)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED COMPONENTS core imgproc features2d calib3d photo)

include_directories(include ${OpenCV_INCLUDE_DIRS})

add_executable(pano_stitch_node
  src/pano_stitch_node.cpp
  src/stitcher.cpp
)

ament_target_dependencies(pano_stitch_node
  rclcpp
  sensor_msgs
  std_msgs
  std_srvs
  cv_bridge
  image_transport
  OpenCV
)

target_link_libraries(pano_stitch_node ${OpenCV_LIBS})

install(TARGETS
  pano_stitch_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
