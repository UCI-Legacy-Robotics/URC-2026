// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice
#include "drive_teleop/msg/detail/drive_control_message__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
drive_teleop__msg__DriveControlMessage__init(drive_teleop__msg__DriveControlMessage * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    drive_teleop__msg__DriveControlMessage__fini(msg);
    return false;
  }
  // left_input_pwm
  // right_input_pwm
  return true;
}

void
drive_teleop__msg__DriveControlMessage__fini(drive_teleop__msg__DriveControlMessage * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // left_input_pwm
  // right_input_pwm
}

bool
drive_teleop__msg__DriveControlMessage__are_equal(const drive_teleop__msg__DriveControlMessage * lhs, const drive_teleop__msg__DriveControlMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // left_input_pwm
  if (lhs->left_input_pwm != rhs->left_input_pwm) {
    return false;
  }
  // right_input_pwm
  if (lhs->right_input_pwm != rhs->right_input_pwm) {
    return false;
  }
  return true;
}

bool
drive_teleop__msg__DriveControlMessage__copy(
  const drive_teleop__msg__DriveControlMessage * input,
  drive_teleop__msg__DriveControlMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // left_input_pwm
  output->left_input_pwm = input->left_input_pwm;
  // right_input_pwm
  output->right_input_pwm = input->right_input_pwm;
  return true;
}

drive_teleop__msg__DriveControlMessage *
drive_teleop__msg__DriveControlMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drive_teleop__msg__DriveControlMessage * msg = (drive_teleop__msg__DriveControlMessage *)allocator.allocate(sizeof(drive_teleop__msg__DriveControlMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drive_teleop__msg__DriveControlMessage));
  bool success = drive_teleop__msg__DriveControlMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drive_teleop__msg__DriveControlMessage__destroy(drive_teleop__msg__DriveControlMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drive_teleop__msg__DriveControlMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drive_teleop__msg__DriveControlMessage__Sequence__init(drive_teleop__msg__DriveControlMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drive_teleop__msg__DriveControlMessage * data = NULL;

  if (size) {
    data = (drive_teleop__msg__DriveControlMessage *)allocator.zero_allocate(size, sizeof(drive_teleop__msg__DriveControlMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drive_teleop__msg__DriveControlMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drive_teleop__msg__DriveControlMessage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drive_teleop__msg__DriveControlMessage__Sequence__fini(drive_teleop__msg__DriveControlMessage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drive_teleop__msg__DriveControlMessage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drive_teleop__msg__DriveControlMessage__Sequence *
drive_teleop__msg__DriveControlMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drive_teleop__msg__DriveControlMessage__Sequence * array = (drive_teleop__msg__DriveControlMessage__Sequence *)allocator.allocate(sizeof(drive_teleop__msg__DriveControlMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drive_teleop__msg__DriveControlMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drive_teleop__msg__DriveControlMessage__Sequence__destroy(drive_teleop__msg__DriveControlMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drive_teleop__msg__DriveControlMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drive_teleop__msg__DriveControlMessage__Sequence__are_equal(const drive_teleop__msg__DriveControlMessage__Sequence * lhs, const drive_teleop__msg__DriveControlMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drive_teleop__msg__DriveControlMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drive_teleop__msg__DriveControlMessage__Sequence__copy(
  const drive_teleop__msg__DriveControlMessage__Sequence * input,
  drive_teleop__msg__DriveControlMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drive_teleop__msg__DriveControlMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drive_teleop__msg__DriveControlMessage * data =
      (drive_teleop__msg__DriveControlMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drive_teleop__msg__DriveControlMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drive_teleop__msg__DriveControlMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drive_teleop__msg__DriveControlMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
