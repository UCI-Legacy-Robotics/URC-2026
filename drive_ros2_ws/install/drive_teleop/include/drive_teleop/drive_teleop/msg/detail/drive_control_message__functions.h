// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice

#ifndef DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__FUNCTIONS_H_
#define DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "drive_teleop/msg/rosidl_generator_c__visibility_control.h"

#include "drive_teleop/msg/detail/drive_control_message__struct.h"

/// Initialize msg/DriveControlMessage message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * drive_teleop__msg__DriveControlMessage
 * )) before or use
 * drive_teleop__msg__DriveControlMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
bool
drive_teleop__msg__DriveControlMessage__init(drive_teleop__msg__DriveControlMessage * msg);

/// Finalize msg/DriveControlMessage message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
void
drive_teleop__msg__DriveControlMessage__fini(drive_teleop__msg__DriveControlMessage * msg);

/// Create msg/DriveControlMessage message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * drive_teleop__msg__DriveControlMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
drive_teleop__msg__DriveControlMessage *
drive_teleop__msg__DriveControlMessage__create();

/// Destroy msg/DriveControlMessage message.
/**
 * It calls
 * drive_teleop__msg__DriveControlMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
void
drive_teleop__msg__DriveControlMessage__destroy(drive_teleop__msg__DriveControlMessage * msg);

/// Check for msg/DriveControlMessage message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
bool
drive_teleop__msg__DriveControlMessage__are_equal(const drive_teleop__msg__DriveControlMessage * lhs, const drive_teleop__msg__DriveControlMessage * rhs);

/// Copy a msg/DriveControlMessage message.
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
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
bool
drive_teleop__msg__DriveControlMessage__copy(
  const drive_teleop__msg__DriveControlMessage * input,
  drive_teleop__msg__DriveControlMessage * output);

/// Initialize array of msg/DriveControlMessage messages.
/**
 * It allocates the memory for the number of elements and calls
 * drive_teleop__msg__DriveControlMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
bool
drive_teleop__msg__DriveControlMessage__Sequence__init(drive_teleop__msg__DriveControlMessage__Sequence * array, size_t size);

/// Finalize array of msg/DriveControlMessage messages.
/**
 * It calls
 * drive_teleop__msg__DriveControlMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
void
drive_teleop__msg__DriveControlMessage__Sequence__fini(drive_teleop__msg__DriveControlMessage__Sequence * array);

/// Create array of msg/DriveControlMessage messages.
/**
 * It allocates the memory for the array and calls
 * drive_teleop__msg__DriveControlMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
drive_teleop__msg__DriveControlMessage__Sequence *
drive_teleop__msg__DriveControlMessage__Sequence__create(size_t size);

/// Destroy array of msg/DriveControlMessage messages.
/**
 * It calls
 * drive_teleop__msg__DriveControlMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
void
drive_teleop__msg__DriveControlMessage__Sequence__destroy(drive_teleop__msg__DriveControlMessage__Sequence * array);

/// Check for msg/DriveControlMessage message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
bool
drive_teleop__msg__DriveControlMessage__Sequence__are_equal(const drive_teleop__msg__DriveControlMessage__Sequence * lhs, const drive_teleop__msg__DriveControlMessage__Sequence * rhs);

/// Copy an array of msg/DriveControlMessage messages.
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
ROSIDL_GENERATOR_C_PUBLIC_drive_teleop
bool
drive_teleop__msg__DriveControlMessage__Sequence__copy(
  const drive_teleop__msg__DriveControlMessage__Sequence * input,
  drive_teleop__msg__DriveControlMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__FUNCTIONS_H_
