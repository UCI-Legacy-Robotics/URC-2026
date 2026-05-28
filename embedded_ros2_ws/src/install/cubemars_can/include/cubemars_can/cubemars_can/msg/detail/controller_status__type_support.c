// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "cubemars_can/msg/detail/controller_status__rosidl_typesupport_introspection_c.h"
#include "cubemars_can/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "cubemars_can/msg/detail/controller_status__functions.h"
#include "cubemars_can/msg/detail/controller_status__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  cubemars_can__msg__ControllerStatus__init(message_memory);
}

void cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_fini_function(void * message_memory)
{
  cubemars_can__msg__ControllerStatus__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_member_array[5] = {
  {
    "pos_estimate_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cubemars_can__msg__ControllerStatus, pos_estimate_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "vel_estimate_rpm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cubemars_can__msg__ControllerStatus, vel_estimate_rpm),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motor_current_amps",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cubemars_can__msg__ControllerStatus, motor_current_amps),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motor_temperature_c",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cubemars_can__msg__ControllerStatus, motor_temperature_c),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "active_errors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(cubemars_can__msg__ControllerStatus, active_errors),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_members = {
  "cubemars_can__msg",  // message namespace
  "ControllerStatus",  // message name
  5,  // number of fields
  sizeof(cubemars_can__msg__ControllerStatus),
  cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_member_array,  // message members
  cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_type_support_handle = {
  0,
  &cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_cubemars_can
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, cubemars_can, msg, ControllerStatus)() {
  if (!cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_type_support_handle.typesupport_identifier) {
    cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &cubemars_can__msg__ControllerStatus__rosidl_typesupport_introspection_c__ControllerStatus_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
