// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice
#include "cubemars_can/msg/detail/controller_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
cubemars_can__msg__ControllerStatus__init(cubemars_can__msg__ControllerStatus * msg)
{
  if (!msg) {
    return false;
  }
  // pos_estimate_deg
  // vel_estimate_rpm
  // motor_current_amps
  // motor_temperature_c
  // active_errors
  return true;
}

void
cubemars_can__msg__ControllerStatus__fini(cubemars_can__msg__ControllerStatus * msg)
{
  if (!msg) {
    return;
  }
  // pos_estimate_deg
  // vel_estimate_rpm
  // motor_current_amps
  // motor_temperature_c
  // active_errors
}

bool
cubemars_can__msg__ControllerStatus__are_equal(const cubemars_can__msg__ControllerStatus * lhs, const cubemars_can__msg__ControllerStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pos_estimate_deg
  if (lhs->pos_estimate_deg != rhs->pos_estimate_deg) {
    return false;
  }
  // vel_estimate_rpm
  if (lhs->vel_estimate_rpm != rhs->vel_estimate_rpm) {
    return false;
  }
  // motor_current_amps
  if (lhs->motor_current_amps != rhs->motor_current_amps) {
    return false;
  }
  // motor_temperature_c
  if (lhs->motor_temperature_c != rhs->motor_temperature_c) {
    return false;
  }
  // active_errors
  if (lhs->active_errors != rhs->active_errors) {
    return false;
  }
  return true;
}

bool
cubemars_can__msg__ControllerStatus__copy(
  const cubemars_can__msg__ControllerStatus * input,
  cubemars_can__msg__ControllerStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // pos_estimate_deg
  output->pos_estimate_deg = input->pos_estimate_deg;
  // vel_estimate_rpm
  output->vel_estimate_rpm = input->vel_estimate_rpm;
  // motor_current_amps
  output->motor_current_amps = input->motor_current_amps;
  // motor_temperature_c
  output->motor_temperature_c = input->motor_temperature_c;
  // active_errors
  output->active_errors = input->active_errors;
  return true;
}

cubemars_can__msg__ControllerStatus *
cubemars_can__msg__ControllerStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cubemars_can__msg__ControllerStatus * msg = (cubemars_can__msg__ControllerStatus *)allocator.allocate(sizeof(cubemars_can__msg__ControllerStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(cubemars_can__msg__ControllerStatus));
  bool success = cubemars_can__msg__ControllerStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
cubemars_can__msg__ControllerStatus__destroy(cubemars_can__msg__ControllerStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    cubemars_can__msg__ControllerStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
cubemars_can__msg__ControllerStatus__Sequence__init(cubemars_can__msg__ControllerStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cubemars_can__msg__ControllerStatus * data = NULL;

  if (size) {
    data = (cubemars_can__msg__ControllerStatus *)allocator.zero_allocate(size, sizeof(cubemars_can__msg__ControllerStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = cubemars_can__msg__ControllerStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        cubemars_can__msg__ControllerStatus__fini(&data[i - 1]);
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
cubemars_can__msg__ControllerStatus__Sequence__fini(cubemars_can__msg__ControllerStatus__Sequence * array)
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
      cubemars_can__msg__ControllerStatus__fini(&array->data[i]);
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

cubemars_can__msg__ControllerStatus__Sequence *
cubemars_can__msg__ControllerStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  cubemars_can__msg__ControllerStatus__Sequence * array = (cubemars_can__msg__ControllerStatus__Sequence *)allocator.allocate(sizeof(cubemars_can__msg__ControllerStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = cubemars_can__msg__ControllerStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
cubemars_can__msg__ControllerStatus__Sequence__destroy(cubemars_can__msg__ControllerStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    cubemars_can__msg__ControllerStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
cubemars_can__msg__ControllerStatus__Sequence__are_equal(const cubemars_can__msg__ControllerStatus__Sequence * lhs, const cubemars_can__msg__ControllerStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!cubemars_can__msg__ControllerStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
cubemars_can__msg__ControllerStatus__Sequence__copy(
  const cubemars_can__msg__ControllerStatus__Sequence * input,
  cubemars_can__msg__ControllerStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(cubemars_can__msg__ControllerStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    cubemars_can__msg__ControllerStatus * data =
      (cubemars_can__msg__ControllerStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!cubemars_can__msg__ControllerStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          cubemars_can__msg__ControllerStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!cubemars_can__msg__ControllerStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
