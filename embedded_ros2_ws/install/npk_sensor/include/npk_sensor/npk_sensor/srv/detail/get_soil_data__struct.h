// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice

#ifndef NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__STRUCT_H_
#define NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetSoilData in the package npk_sensor.
typedef struct npk_sensor__srv__GetSoilData_Request
{
  uint8_t structure_needs_at_least_one_member;
} npk_sensor__srv__GetSoilData_Request;

// Struct for a sequence of npk_sensor__srv__GetSoilData_Request.
typedef struct npk_sensor__srv__GetSoilData_Request__Sequence
{
  npk_sensor__srv__GetSoilData_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} npk_sensor__srv__GetSoilData_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/GetSoilData in the package npk_sensor.
typedef struct npk_sensor__srv__GetSoilData_Response
{
  float ph;
  float moisture;
  float temperature;
  float conductivity;
  float nitrogen;
  float phosphorus;
  float potassium;
} npk_sensor__srv__GetSoilData_Response;

// Struct for a sequence of npk_sensor__srv__GetSoilData_Response.
typedef struct npk_sensor__srv__GetSoilData_Response__Sequence
{
  npk_sensor__srv__GetSoilData_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} npk_sensor__srv__GetSoilData_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__STRUCT_H_
