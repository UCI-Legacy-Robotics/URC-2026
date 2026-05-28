// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from cubemars_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice
#include "cubemars_can/msg/detail/control_message__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
cubemars_can__msg__ControlMessage__init(cubemars_can__msg__ControlMessage * msg)
{
  if (!msg) {
    return false;
  }
  // control_mode
  // input_vel_rpm
  // input_pos_deg
  // set_vel_limit_rpm
  // set_accel_limit_rpm_s
  // set_origin
  return true;
}

void
cubemars_can__msg__ControlMessage__fini(cubemars_can__msg__ControlMessage * msg)
{
  if (!msg) {
    return;
  }
  // control_mode
  // input_vel_rpm
  // input_pos_deg
  // set_vel_limit_rpm
  // set_accel_limit_rpm_s
  // set_origin
}

bool
cubemars_can__msg__ControlMessage__are_equal(const cubemars_can__msg__ControlMessage * lhs, const cubemars_can__msg__ControlMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // control_mode
  if (lhs->control_mode != rhs->control_mode) {
    return false;
  }
  // input_vel_rpm
  if (lhs->input_vel_rpm != rhs->input_vel_rpm) {
    return false;
  }
  // input_pos_deg
  if (lhs->input_pos_deg != rhs->input_pos_deg) {
    return false;
  }
  // set_vel_limit_rpm
  if (lhs->set_vel_limit_rpm != rhs->set_vel_limit_rpm) {
    return false;
  }
  // set_accel_limit_rpm_s
  if (lhs->set_accel_limit_rpm_s != rhs->set_accel_limit_rpm_s) {
    return false;
  }
  // set_origin
  if (lhs->set_origin != rhs->set_origin) {
    return false;
  }
  return true;
}

bool
cubemars_can__msg__ControlMessage__copy(
  const cubemars_can__msg__ControlMessage * input,
  cubemars_can__msg__ControlMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // control_mode
  output->control_mode = input->control_mode;
  // input_vel_rpm
  output->input_vel_rpm = input->input_vel_rpm;
  // input_pos_deg
  output->input_pos_deg = input->input_pos_deg;
  // set_vel_limit_rpm
  output->set_vel_limit_rpm = input->set_vel_limit_rpm;
  // set_accel_limit_rpm_s
  output->set_accel_limit_rpm_s = input->set_accel_limit_rpm_s;
  // set_origin
  output->set_origin = input->set_origin;
  return true;
}

cubemars_can__msg__ControlMessage *
cubemars_can__msg__ControlMessage__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cubemars_can__msg__ControlMessage * msg = (cubemars_can__msg__ControlMessage *)allocator.allocate(sizeof(cubemars_can__msg__ControlMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cubemars_can__msg__ControlMessage));
  bool success = cubemars_can__msg__ControlMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cubemars_can__msg__ControlMessage__destroy(cubemars_can__msg__ControlMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cubemars_can__msg__ControlMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cubemars_can__msg__ControlMessage__Sequence__init(cubemars_can__msg__ControlMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cubemars_can__msg__ControlMessage * data = NULL;

  if (size) {
    data = (cubemars_can__msg__ControlMessage *)allocator.zero_allocate(size, sizeof(cubemars_can__msg__ControlMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cubemars_can__msg__ControlMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cubemars_can__msg__ControlMessage__fini(&data[i - 1]);
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
cubemars_can__msg__ControlMessage__Sequence__fini(cubemars_can__msg__ControlMessage__Sequence * array)
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
      cubemars_can__msg__ControlMessage__fini(&array->data[i]);
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

cubemars_can__msg__ControlMessage__Sequence *
cubemars_can__msg__ControlMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cubemars_can__msg__ControlMessage__Sequence * array = (cubemars_can__msg__ControlMessage__Sequence *)allocator.allocate(sizeof(cubemars_can__msg__ControlMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cubemars_can__msg__ControlMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cubemars_can__msg__ControlMessage__Sequence__destroy(cubemars_can__msg__ControlMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cubemars_can__msg__ControlMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cubemars_can__msg__ControlMessage__Sequence__are_equal(const cubemars_can__msg__ControlMessage__Sequence * lhs, const cubemars_can__msg__ControlMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cubemars_can__msg__ControlMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cubemars_can__msg__ControlMessage__Sequence__copy(
  const cubemars_can__msg__ControlMessage__Sequence * input,
  cubemars_can__msg__ControlMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cubemars_can__msg__ControlMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    cubemars_can__msg__ControlMessage * data =
      (cubemars_can__msg__ControlMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cubemars_can__msg__ControlMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          cubemars_can__msg__ControlMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cubemars_can__msg__ControlMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
