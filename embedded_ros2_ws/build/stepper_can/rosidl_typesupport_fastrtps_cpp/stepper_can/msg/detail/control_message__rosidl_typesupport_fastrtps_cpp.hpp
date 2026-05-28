// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from stepper_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "stepper_can/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "stepper_can/msg/detail/control_message__struct.hpp"

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

namespace stepper_can
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stepper_can
cdr_serialize(
  const stepper_can::msg::ControlMessage & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stepper_can
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  stepper_can::msg::ControlMessage & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stepper_can
get_serialized_size(
  const stepper_can::msg::ControlMessage & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stepper_can
max_serialized_size_ControlMessage(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace stepper_can

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_stepper_can
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, stepper_can, msg, ControlMessage)();

#ifdef __cplusplus
}
#endif

#endif  // STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
