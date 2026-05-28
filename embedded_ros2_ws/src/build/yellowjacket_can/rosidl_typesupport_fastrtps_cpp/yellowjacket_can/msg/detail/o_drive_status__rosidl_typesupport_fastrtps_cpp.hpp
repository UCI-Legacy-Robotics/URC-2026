// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from yellowjacket_can:msg/ODriveStatus.idl
// generated code does not contain a copyright notice

#ifndef YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "yellowjacket_can/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "yellowjacket_can/msg/detail/o_drive_status__struct.hpp"

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

namespace yellowjacket_can
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_yellowjacket_can
cdr_serialize(
  const yellowjacket_can::msg::ODriveStatus & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_yellowjacket_can
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  yellowjacket_can::msg::ODriveStatus & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_yellowjacket_can
get_serialized_size(
  const yellowjacket_can::msg::ODriveStatus & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_yellowjacket_can
max_serialized_size_ODriveStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace yellowjacket_can

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_yellowjacket_can
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, yellowjacket_can, msg, ODriveStatus)();

#ifdef __cplusplus
}
#endif

#endif  // YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
