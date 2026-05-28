// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from stepper_can:msg/ODriveStatus.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__MSG__DETAIL__O_DRIVE_STATUS__STRUCT_H_
#define STEPPER_CAN__MSG__DETAIL__O_DRIVE_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ODriveStatus in the package stepper_can.
typedef struct stepper_can__msg__ODriveStatus
{
  float bus_voltage;
  float bus_current;
  float fet_temperature;
  float motor_temperature;
  uint32_t active_errors;
  uint32_t disarm_reason;
} stepper_can__msg__ODriveStatus;

// Struct for a sequence of stepper_can__msg__ODriveStatus.
typedef struct stepper_can__msg__ODriveStatus__Sequence
{
  stepper_can__msg__ODriveStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} stepper_can__msg__ODriveStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // STEPPER_CAN__MSG__DETAIL__O_DRIVE_STATUS__STRUCT_H_
