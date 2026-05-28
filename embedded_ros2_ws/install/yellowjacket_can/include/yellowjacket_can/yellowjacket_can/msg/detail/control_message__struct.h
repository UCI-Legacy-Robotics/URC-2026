// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from yellowjacket_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef YELLOWJACKET_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
#define YELLOWJACKET_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ControlMessage in the package yellowjacket_can.
typedef struct yellowjacket_can__msg__ControlMessage
{
  uint32_t control_mode;
  uint32_t input_mode;
  int32_t input_pos;
  int32_t input_vel;
  int32_t input_torque;
} yellowjacket_can__msg__ControlMessage;

// Struct for a sequence of yellowjacket_can__msg__ControlMessage.
typedef struct yellowjacket_can__msg__ControlMessage__Sequence
{
  yellowjacket_can__msg__ControlMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yellowjacket_can__msg__ControlMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // YELLOWJACKET_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
