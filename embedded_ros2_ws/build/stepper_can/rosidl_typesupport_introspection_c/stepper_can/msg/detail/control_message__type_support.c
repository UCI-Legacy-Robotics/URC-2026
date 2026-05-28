// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from stepper_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "stepper_can/msg/detail/control_message__rosidl_typesupport_introspection_c.h"
#include "stepper_can/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "stepper_can/msg/detail/control_message__functions.h"
#include "stepper_can/msg/detail/control_message__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  stepper_can__msg__ControlMessage__init(message_memory);
}

void stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_fini_function(void * message_memory)
{
  stepper_can__msg__ControlMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_member_array[5] = {
  {
    "control_mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(stepper_can__msg__ControlMessage, control_mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "input_mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(stepper_can__msg__ControlMessage, input_mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "input_pos",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(stepper_can__msg__ControlMessage, input_pos),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "input_vel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(stepper_can__msg__ControlMessage, input_vel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "input_torque",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(stepper_can__msg__ControlMessage, input_torque),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_members = {
  "stepper_can__msg",  // message namespace
  "ControlMessage",  // message name
  5,  // number of fields
  sizeof(stepper_can__msg__ControlMessage),
  stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_member_array,  // message members
  stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_type_support_handle = {
  0,
  &stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_stepper_can
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, stepper_can, msg, ControlMessage)() {
  if (!stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_type_support_handle.typesupport_identifier) {
    stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &stepper_can__msg__ControlMessage__rosidl_typesupport_introspection_c__ControlMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
