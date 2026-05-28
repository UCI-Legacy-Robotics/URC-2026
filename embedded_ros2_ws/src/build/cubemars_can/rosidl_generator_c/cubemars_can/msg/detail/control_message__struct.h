// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cubemars_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ControlMessage in the package cubemars_can.
typedef struct cubemars_can__msg__ControlMessage
{
  uint32_t control_mode;
  float input_vel_rpm;
  float input_pos_deg;
  float set_vel_limit_rpm;
  float set_accel_limit_rpm_s;
  uint8_t set_origin;
} cubemars_can__msg__ControlMessage;

// Struct for a sequence of cubemars_can__msg__ControlMessage.
typedef struct cubemars_can__msg__ControlMessage__Sequence
{
  cubemars_can__msg__ControlMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cubemars_can__msg__ControlMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_H_
