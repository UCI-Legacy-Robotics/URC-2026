find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GetSoilData.srv"
)

add_executable(npk_node src/npk_node.cpp)
ament_target_dependencies(npk_node rclcpp)

rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(npk_node "${cpp_typesupport_target}")

install(TARGETS
  npk_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
