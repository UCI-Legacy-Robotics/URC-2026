cmake_minimum_required(VERSION 3.8)
project(science)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(stepper_can REQUIRED)
find_package(stepper_node REQUIRED)
find_package(servo REQUIRED)
find_package(odrive_node REQUIRED)
find_package(npk_sensor REQUIRED)

# stepper_controller node
add_executable(stepper_controller src/scienceController.cpp)
ament_target_dependencies(stepper_controller
  rclcpp
  std_msgs
  std_srvs
  stepper_can
  stepper_node
  servo
  odrive_node
)

# science_logic node
add_executable(science_logic src/ScienceLogic.cpp)
ament_target_dependencies(science_logic
  rclcpp
  std_msgs
  npk_sensor
)

install(TARGETS
  stepper_controller
  science_logic
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()