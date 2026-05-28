// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice

#ifndef DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__STRUCT_H_
#define DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/DriveControlMessage in the package drive_teleop.
typedef struct drive_teleop__msg__DriveControlMessage
{
  std_msgs__msg__Header header;
  int32_t left_input_pwm;
  int32_t right_input_pwm;
} drive_teleop__msg__DriveControlMessage;

// Struct for a sequence of drive_teleop__msg__DriveControlMessage.
typedef struct drive_teleop__msg__DriveControlMessage__Sequence
{
  drive_teleop__msg__DriveControlMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drive_teleop__msg__DriveControlMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__STRUCT_H_
