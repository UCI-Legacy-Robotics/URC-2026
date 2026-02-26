cmake_minimum_required(VERSION 3.8)
project(npk_sensor)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GetSoilData.srv"
)

# Install Python package
ament_python_install_package(soil_sensor)

# 3. Create the "Console Entry" (The setup.py 'entry_points' equivalent)
# This creates an executable named 'npk_node' in the lib folder
# for use through ros2 run...
install(PROGRAMS soil_sensor/npk_sensor_node.py 
        DESTINATION lib/${PROJECT_NAME} 
        RENAME npk_node)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
