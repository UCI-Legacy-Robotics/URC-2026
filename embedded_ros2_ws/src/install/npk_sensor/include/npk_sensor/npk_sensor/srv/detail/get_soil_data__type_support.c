// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "npk_sensor/srv/detail/get_soil_data__rosidl_typesupport_introspection_c.h"
#include "npk_sensor/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "npk_sensor/srv/detail/get_soil_data__functions.h"
#include "npk_sensor/srv/detail/get_soil_data__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  npk_sensor__srv__GetSoilData_Request__init(message_memory);
}

void npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_fini_function(void * message_memory)
{
  npk_sensor__srv__GetSoilData_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_members = {
  "npk_sensor__srv",  // message namespace
  "GetSoilData_Request",  // message name
  1,  // number of fields
  sizeof(npk_sensor__srv__GetSoilData_Request),
  npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_member_array,  // message members
  npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_type_support_handle = {
  0,
  &npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_npk_sensor
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData_Request)() {
  if (!npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_type_support_handle.typesupport_identifier) {
    npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &npk_sensor__srv__GetSoilData_Request__rosidl_typesupport_introspection_c__GetSoilData_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "npk_sensor/srv/detail/get_soil_data__rosidl_typesupport_introspection_c.h"
// already included above
// #include "npk_sensor/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "npk_sensor/srv/detail/get_soil_data__functions.h"
// already included above
// #include "npk_sensor/srv/detail/get_soil_data__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  npk_sensor__srv__GetSoilData_Response__init(message_memory);
}

void npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_fini_function(void * message_memory)
{
  npk_sensor__srv__GetSoilData_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_member_array[7] = {
  {
    "ph",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, ph),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "moisture",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, moisture),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "temperature",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, temperature),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "conductivity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, conductivity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "nitrogen",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, nitrogen),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "phosphorus",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, phosphorus),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "potassium",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(npk_sensor__srv__GetSoilData_Response, potassium),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_members = {
  "npk_sensor__srv",  // message namespace
  "GetSoilData_Response",  // message name
  7,  // number of fields
  sizeof(npk_sensor__srv__GetSoilData_Response),
  npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_member_array,  // message members
  npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_type_support_handle = {
  0,
  &npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_npk_sensor
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData_Response)() {
  if (!npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_type_support_handle.typesupport_identifier) {
    npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &npk_sensor__srv__GetSoilData_Response__rosidl_typesupport_introspection_c__GetSoilData_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "npk_sensor/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "npk_sensor/srv/detail/get_soil_data__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_members = {
  "npk_sensor__srv",  // service namespace
  "GetSoilData",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_Request_message_type_support_handle,
  NULL  // response message
  // npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_Response_message_type_support_handle
};

static rosidl_service_type_support_t npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_type_support_handle = {
  0,
  &npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_npk_sensor
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData)() {
  if (!npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_type_support_handle.typesupport_identifier) {
    npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, npk_sensor, srv, GetSoilData_Response)()->data;
  }

  return &npk_sensor__srv__detail__get_soil_data__rosidl_typesupport_introspection_c__GetSoilData_service_type_support_handle;
}
