// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from stepper_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
#define STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ControlMessage in the package stepper_can.
typedef struct stepper_can__msg__ControlMessage
{
  uint32_t control_mode;
  uint32_t input_mode;
  int32_t input_pos;
  int32_t input_vel;
  int32_t input_torque;
} stepper_can__msg__ControlMessage;

// Struct for a sequence of stepper_can__msg__ControlMessage.
typedef struct stepper_can__msg__ControlMessage__Sequence
{
  stepper_can__msg__ControlMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} stepper_can__msg__ControlMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
