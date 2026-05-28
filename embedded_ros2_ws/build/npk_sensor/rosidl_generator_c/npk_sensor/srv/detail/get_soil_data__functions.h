// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice

#ifndef NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__FUNCTIONS_H_
#define NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "npk_sensor/msg/rosidl_generator_c__visibility_control.h"

#include "npk_sensor/srv/detail/get_soil_data__struct.h"

/// Initialize srv/GetSoilData message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * npk_sensor__srv__GetSoilData_Request
 * )) before or use
 * npk_sensor__srv__GetSoilData_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Request__init(npk_sensor__srv__GetSoilData_Request * msg);

/// Finalize srv/GetSoilData message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Request__fini(npk_sensor__srv__GetSoilData_Request * msg);

/// Create srv/GetSoilData message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * npk_sensor__srv__GetSoilData_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
npk_sensor__srv__GetSoilData_Request *
npk_sensor__srv__GetSoilData_Request__create();

/// Destroy srv/GetSoilData message.
/**
 * It calls
 * npk_sensor__srv__GetSoilData_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Request__destroy(npk_sensor__srv__GetSoilData_Request * msg);

/// Check for srv/GetSoilData message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Request__are_equal(const npk_sensor__srv__GetSoilData_Request * lhs, const npk_sensor__srv__GetSoilData_Request * rhs);

/// Copy a srv/GetSoilData message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Request__copy(
  const npk_sensor__srv__GetSoilData_Request * input,
  npk_sensor__srv__GetSoilData_Request * output);

/// Initialize array of srv/GetSoilData messages.
/**
 * It allocates the memory for the number of elements and calls
 * npk_sensor__srv__GetSoilData_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Request__Sequence__init(npk_sensor__srv__GetSoilData_Request__Sequence * array, size_t size);

/// Finalize array of srv/GetSoilData messages.
/**
 * It calls
 * npk_sensor__srv__GetSoilData_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Request__Sequence__fini(npk_sensor__srv__GetSoilData_Request__Sequence * array);

/// Create array of srv/GetSoilData messages.
/**
 * It allocates the memory for the array and calls
 * npk_sensor__srv__GetSoilData_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
npk_sensor__srv__GetSoilData_Request__Sequence *
npk_sensor__srv__GetSoilData_Request__Sequence__create(size_t size);

/// Destroy array of srv/GetSoilData messages.
/**
 * It calls
 * npk_sensor__srv__GetSoilData_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Request__Sequence__destroy(npk_sensor__srv__GetSoilData_Request__Sequence * array);

/// Check for srv/GetSoilData message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Request__Sequence__are_equal(const npk_sensor__srv__GetSoilData_Request__Sequence * lhs, const npk_sensor__srv__GetSoilData_Request__Sequence * rhs);

/// Copy an array of srv/GetSoilData messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Request__Sequence__copy(
  const npk_sensor__srv__GetSoilData_Request__Sequence * input,
  npk_sensor__srv__GetSoilData_Request__Sequence * output);

/// Initialize srv/GetSoilData message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * npk_sensor__srv__GetSoilData_Response
 * )) before or use
 * npk_sensor__srv__GetSoilData_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Response__init(npk_sensor__srv__GetSoilData_Response * msg);

/// Finalize srv/GetSoilData message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Response__fini(npk_sensor__srv__GetSoilData_Response * msg);

/// Create srv/GetSoilData message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * npk_sensor__srv__GetSoilData_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
npk_sensor__srv__GetSoilData_Response *
npk_sensor__srv__GetSoilData_Response__create();

/// Destroy srv/GetSoilData message.
/**
 * It calls
 * npk_sensor__srv__GetSoilData_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Response__destroy(npk_sensor__srv__GetSoilData_Response * msg);

/// Check for srv/GetSoilData message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Response__are_equal(const npk_sensor__srv__GetSoilData_Response * lhs, const npk_sensor__srv__GetSoilData_Response * rhs);

/// Copy a srv/GetSoilData message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Response__copy(
  const npk_sensor__srv__GetSoilData_Response * input,
  npk_sensor__srv__GetSoilData_Response * output);

/// Initialize array of srv/GetSoilData messages.
/**
 * It allocates the memory for the number of elements and calls
 * npk_sensor__srv__GetSoilData_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Response__Sequence__init(npk_sensor__srv__GetSoilData_Response__Sequence * array, size_t size);

/// Finalize array of srv/GetSoilData messages.
/**
 * It calls
 * npk_sensor__srv__GetSoilData_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Response__Sequence__fini(npk_sensor__srv__GetSoilData_Response__Sequence * array);

/// Create array of srv/GetSoilData messages.
/**
 * It allocates the memory for the array and calls
 * npk_sensor__srv__GetSoilData_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
npk_sensor__srv__GetSoilData_Response__Sequence *
npk_sensor__srv__GetSoilData_Response__Sequence__create(size_t size);

/// Destroy array of srv/GetSoilData messages.
/**
 * It calls
 * npk_sensor__srv__GetSoilData_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
void
npk_sensor__srv__GetSoilData_Response__Sequence__destroy(npk_sensor__srv__GetSoilData_Response__Sequence * array);

/// Check for srv/GetSoilData message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Response__Sequence__are_equal(const npk_sensor__srv__GetSoilData_Response__Sequence * lhs, const npk_sensor__srv__GetSoilData_Response__Sequence * rhs);

/// Copy an array of srv/GetSoilData messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_npk_sensor
bool
npk_sensor__srv__GetSoilData_Response__Sequence__copy(
  const npk_sensor__srv__GetSoilData_Response__Sequence * input,
  npk_sensor__srv__GetSoilData_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__FUNCTIONS_H_
