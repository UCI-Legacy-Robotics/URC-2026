// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "cubemars_can/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "cubemars_can/msg/detail/controller_status__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace cubemars_can
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cubemars_can
cdr_serialize(
  const cubemars_can::msg::ControllerStatus & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cubemars_can
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  cubemars_can::msg::ControllerStatus & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cubemars_can
get_serialized_size(
  const cubemars_can::msg::ControllerStatus & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cubemars_can
max_serialized_size_ControllerStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace cubemars_can

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_cubemars_can
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, cubemars_can, msg, ControllerStatus)();

#ifdef __cplusplus
}
#endif

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
