// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__STRUCT_H_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ControllerStatus in the package cubemars_can.
typedef struct cubemars_can__msg__ControllerStatus
{
  float pos_estimate_deg;
  float vel_estimate_rpm;
  float motor_current_amps;
  int8_t motor_temperature_c;
  uint8_t active_errors;
} cubemars_can__msg__ControllerStatus;

// Struct for a sequence of cubemars_can__msg__ControllerStatus.
typedef struct cubemars_can__msg__ControllerStatus__Sequence
{
  cubemars_can__msg__ControllerStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} cubemars_can__msg__ControllerStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__STRUCT_H_
