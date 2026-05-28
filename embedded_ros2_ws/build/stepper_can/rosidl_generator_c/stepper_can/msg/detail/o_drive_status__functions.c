// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from stepper_can:msg/ODriveStatus.idl
// generated code does not contain a copyright notice
#include "stepper_can/msg/detail/o_drive_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
stepper_can__msg__ODriveStatus__init(stepper_can__msg__ODriveStatus * msg)
{
  if (!msg) {
    return false;
  }
  // bus_voltage
  // bus_current
  // fet_temperature
  // motor_temperature
  // active_errors
  // disarm_reason
  return true;
}

void
stepper_can__msg__ODriveStatus__fini(stepper_can__msg__ODriveStatus * msg)
{
  if (!msg) {
    return;
  }
  // bus_voltage
  // bus_current
  // fet_temperature
  // motor_temperature
  // active_errors
  // disarm_reason
}

bool
stepper_can__msg__ODriveStatus__are_equal(const stepper_can__msg__ODriveStatus * lhs, const stepper_can__msg__ODriveStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // bus_voltage
  if (lhs->bus_voltage != rhs->bus_voltage) {
    return false;
  }
  // bus_current
  if (lhs->bus_current != rhs->bus_current) {
    return false;
  }
  // fet_temperature
  if (lhs->fet_temperature != rhs->fet_temperature) {
    return false;
  }
  // motor_temperature
  if (lhs->motor_temperature != rhs->motor_temperature) {
    return false;
  }
  // active_errors
  if (lhs->active_errors != rhs->active_errors) {
    return false;
  }
  // disarm_reason
  if (lhs->disarm_reason != rhs->disarm_reason) {
    return false;
  }
  return true;
}

bool
stepper_can__msg__ODriveStatus__copy(
  const stepper_can__msg__ODriveStatus * input,
  stepper_can__msg__ODriveStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // bus_voltage
  output->bus_voltage = input->bus_voltage;
  // bus_current
  output->bus_current = input->bus_current;
  // fet_temperature
  output->fet_temperature = input->fet_temperature;
  // motor_temperature
  output->motor_temperature = input->motor_temperature;
  // active_errors
  output->active_errors = input->active_errors;
  // disarm_reason
  output->disarm_reason = input->disarm_reason;
  return true;
}

stepper_can__msg__ODriveStatus *
stepper_can__msg__ODriveStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__msg__ODriveStatus * msg = (stepper_can__msg__ODriveStatus *)allocator.allocate(sizeof(stepper_can__msg__ODriveStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(stepper_can__msg__ODriveStatus));
  bool success = stepper_can__msg__ODriveStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
stepper_can__msg__ODriveStatus__destroy(stepper_can__msg__ODriveStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    stepper_can__msg__ODriveStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
stepper_can__msg__ODriveStatus__Sequence__init(stepper_can__msg__ODriveStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__msg__ODriveStatus * data = NULL;

  if (size) {
    data = (stepper_can__msg__ODriveStatus *)allocator.zero_allocate(size, sizeof(stepper_can__msg__ODriveStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = stepper_can__msg__ODriveStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        stepper_can__msg__ODriveStatus__fini(&data[i - 1]);
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
stepper_can__msg__ODriveStatus__Sequence__fini(stepper_can__msg__ODriveStatus__Sequence * array)
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
      stepper_can__msg__ODriveStatus__fini(&array->data[i]);
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

stepper_can__msg__ODriveStatus__Sequence *
stepper_can__msg__ODriveStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__msg__ODriveStatus__Sequence * array = (stepper_can__msg__ODriveStatus__Sequence *)allocator.allocate(sizeof(stepper_can__msg__ODriveStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = stepper_can__msg__ODriveStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
stepper_can__msg__ODriveStatus__Sequence__destroy(stepper_can__msg__ODriveStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    stepper_can__msg__ODriveStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
stepper_can__msg__ODriveStatus__Sequence__are_equal(const stepper_can__msg__ODriveStatus__Sequence * lhs, const stepper_can__msg__ODriveStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!stepper_can__msg__ODriveStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
stepper_can__msg__ODriveStatus__Sequence__copy(
  const stepper_can__msg__ODriveStatus__Sequence * input,
  stepper_can__msg__ODriveStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(stepper_can__msg__ODriveStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    stepper_can__msg__ODriveStatus * data =
      (stepper_can__msg__ODriveStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!stepper_can__msg__ODriveStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          stepper_can__msg__ODriveStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!stepper_can__msg__ODriveStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
