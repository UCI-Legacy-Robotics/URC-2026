// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from stepper_can:srv/AxisState.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__SRV__DETAIL__AXIS_STATE__STRUCT_H_
#define STEPPER_CAN__SRV__DETAIL__AXIS_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/AxisState in the package stepper_can.
typedef struct stepper_can__srv__AxisState_Request
{
  uint32_t axis_requested_state;
} stepper_can__srv__AxisState_Request;

// Struct for a sequence of stepper_can__srv__AxisState_Request.
typedef struct stepper_can__srv__AxisState_Request__Sequence
{
  stepper_can__srv__AxisState_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} stepper_can__srv__AxisState_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/AxisState in the package stepper_can.
typedef struct stepper_can__srv__AxisState_Response
{
  uint32_t active_errors;
  uint8_t axis_state;
  uint8_t procedure_result;
} stepper_can__srv__AxisState_Response;

// Struct for a sequence of stepper_can__srv__AxisState_Response.
typedef struct stepper_can__srv__AxisState_Response__Sequence
{
  stepper_can__srv__AxisState_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} stepper_can__srv__AxisState_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // STEPPER_CAN__SRV__DETAIL__AXIS_STATE__STRUCT_H_
