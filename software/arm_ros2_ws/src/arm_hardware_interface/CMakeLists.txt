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

# Add shared library
add_library(arm_hardware_interface SHARED
  src/arm_hardware_interface.cpp
)

# Export include directory for library
target_include_directories(arm_hardware_interface PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# Add dependencies needed by library (same as package)
ament_target_dependencies(arm_hardware_interface
  rclcpp
  rclcpp_lifecycle
  hardware_interface
  pluginlib
)
  
# Install headers
install(
  DIRECTORY include/
  DESTINATION include
)

# Add targeted include directories for library
install(
  TARGETS arm_hardware_interface
  EXPORT export_arm_hardware_interface
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)

# Export
ament_export_include_directories(include)
ament_export_libraries(arm_hardware_interface)
ament_export_dependencies(hardware_interface rclcpp rclcpp_lifecycle pluginlib)

# Add plugin description
pluginlib_export_plugin_description_file(
  hardware_interface arm_hardware_interface.xml)
    
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
