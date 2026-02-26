cmake_minimum_required(VERSION 3.8)
project(arm_hardware_interface)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies for package
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(cubemars_can REQUIRED)
find_package(odrive_can REQUIRED)
find_package(servo REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

# Add custom message
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ArmTelemetry.msg"
  DEPENDENCIES std_msgs # Ensures std_msgs are found for this custom message
)
ament_export_dependencies(rosidl_default_runtime)

# Add executable node and dependencies
add_executable(arm_driver_node src/arm_driver_node.cpp)
ament_target_dependencies(arm_driver_node
  rclcpp
  cubemars_can
  odrive_can
  servo
  std_msgs
)

# Add shared library
add_library(${PROJECT_NAME}_plugin SHARED
  src/arm_hardware_interface.cpp
)

# Export include directory for library
target_include_directories(${PROJECT_NAME}_plugin PUBLIC
$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
$<INSTALL_INTERFACE:include>
)
# Include for arm driver node too
target_include_directories(arm_driver_node PUBLIC
$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
$<INSTALL_INTERFACE:include>
)

# Add dependencies needed by library (same as package)
ament_target_dependencies(${PROJECT_NAME}_plugin
  rclcpp
  rclcpp_lifecycle
  hardware_interface
  pluginlib
)

# Export plugin description file
pluginlib_export_plugin_description_file(hardware_interface arm_hardware_interface.xml)
  
# Install headers
install(
  DIRECTORY include/
  DESTINATION include
)

# Add targeted include directories for library
install(
  TARGETS ${PROJECT_NAME}_plugin
  EXPORT export_arm_hardware_interface
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)
install(
  TARGETS arm_driver_node
  DESTINATION lib/${PROJECT_NAME}
)

# Export
ament_export_include_directories(include)
ament_export_libraries(a${PROJECT_NAME}_plugin)
ament_export_dependencies(hardware_interface rclcpp rclcpp_lifecycle pluginlib)

# Add plugin description
pluginlib_export_plugin_description_file(
  hardware_interface arm_hardware_interface.xml)

rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(${PROJECT_NAME}_plugin "${cpp_typesupport_target}")
target_link_libraries(arm_driver_node "${cpp_typesupport_target}")
    
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_cmake_gmock REQUIRED)
  find_package(hardware_interface REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
