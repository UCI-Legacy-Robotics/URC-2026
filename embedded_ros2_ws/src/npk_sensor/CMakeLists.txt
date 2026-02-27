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
# Specified directory must contain __init__.py
# Name of directory doesn't have to be src, can be anything but src is clean
ament_python_install_package(src)

# 3. Create the "Console Entry" (The setup.py 'entry_points' equivalent)
# This creates an executable named 'npk_node' in the lib folder
# for use through ros2 run...
install(PROGRAMS src/npk_sensor_node.py 
        DESTINATION lib/${PROJECT_NAME} 
        RENAME npk_node)

# Needed to allow usage of "ros2 launch" of any launch file in launch directory
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
