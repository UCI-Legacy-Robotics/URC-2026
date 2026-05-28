// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice

#ifndef DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "drive_teleop/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "drive_teleop/msg/detail/drive_control_message__struct.hpp"

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

namespace drive_teleop
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drive_teleop
cdr_serialize(
  const drive_teleop::msg::DriveControlMessage & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drive_teleop
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  drive_teleop::msg::DriveControlMessage & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drive_teleop
get_serialized_size(
  const drive_teleop::msg::DriveControlMessage & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drive_teleop
max_serialized_size_DriveControlMessage(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace drive_teleop

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drive_teleop
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, drive_teleop, msg, DriveControlMessage)();

#ifdef __cplusplus
}
#endif

#endif  // DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
