// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from yellowjacket_can:msg/ODriveStatus.idl
// generated code does not contain a copyright notice

#ifndef YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__STRUCT_H_
#define YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ODriveStatus in the package yellowjacket_can.
typedef struct yellowjacket_can__msg__ODriveStatus
{
  float bus_voltage;
  float bus_current;
  float fet_temperature;
  float motor_temperature;
  uint32_t active_errors;
  uint32_t disarm_reason;
} yellowjacket_can__msg__ODriveStatus;

// Struct for a sequence of yellowjacket_can__msg__ODriveStatus.
typedef struct yellowjacket_can__msg__ODriveStatus__Sequence
{
  yellowjacket_can__msg__ODriveStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yellowjacket_can__msg__ODriveStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__STRUCT_H_
