// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from yellowjacket_can:srv/AxisState.idl
// generated code does not contain a copyright notice

#ifndef YELLOWJACKET_CAN__SRV__DETAIL__AXIS_STATE__STRUCT_H_
#define YELLOWJACKET_CAN__SRV__DETAIL__AXIS_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/AxisState in the package yellowjacket_can.
typedef struct yellowjacket_can__srv__AxisState_Request
{
  uint32_t axis_requested_state;
} yellowjacket_can__srv__AxisState_Request;

// Struct for a sequence of yellowjacket_can__srv__AxisState_Request.
typedef struct yellowjacket_can__srv__AxisState_Request__Sequence
{
  yellowjacket_can__srv__AxisState_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yellowjacket_can__srv__AxisState_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/AxisState in the package yellowjacket_can.
typedef struct yellowjacket_can__srv__AxisState_Response
{
  uint32_t active_errors;
  uint8_t axis_state;
  uint8_t procedure_result;
} yellowjacket_can__srv__AxisState_Response;

// Struct for a sequence of yellowjacket_can__srv__AxisState_Response.
typedef struct yellowjacket_can__srv__AxisState_Response__Sequence
{
  yellowjacket_can__srv__AxisState_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} yellowjacket_can__srv__AxisState_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // YELLOWJACKET_CAN__SRV__DETAIL__AXIS_STATE__STRUCT_H_
