// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from servo:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef SERVO__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
#define SERVO__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ControlMessage in the package servo.
typedef struct servo__msg__ControlMessage
{
  uint32_t control_mode;
  float input_vel_deg;
  float input_pos_deg;
} servo__msg__ControlMessage;

// Struct for a sequence of servo__msg__ControlMessage.
typedef struct servo__msg__ControlMessage__Sequence
{
  servo__msg__ControlMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} servo__msg__ControlMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SERVO__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
