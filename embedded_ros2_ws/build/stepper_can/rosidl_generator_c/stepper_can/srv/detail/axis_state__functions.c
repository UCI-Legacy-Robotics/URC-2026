// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from stepper_can:srv/AxisState.idl
// generated code does not contain a copyright notice
#include "stepper_can/srv/detail/axis_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
stepper_can__srv__AxisState_Request__init(stepper_can__srv__AxisState_Request * msg)
{
  if (!msg) {
    return false;
  }
  // axis_requested_state
  return true;
}

void
stepper_can__srv__AxisState_Request__fini(stepper_can__srv__AxisState_Request * msg)
{
  if (!msg) {
    return;
  }
  // axis_requested_state
}

bool
stepper_can__srv__AxisState_Request__are_equal(const stepper_can__srv__AxisState_Request * lhs, const stepper_can__srv__AxisState_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // axis_requested_state
  if (lhs->axis_requested_state != rhs->axis_requested_state) {
    return false;
  }
  return true;
}

bool
stepper_can__srv__AxisState_Request__copy(
  const stepper_can__srv__AxisState_Request * input,
  stepper_can__srv__AxisState_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // axis_requested_state
  output->axis_requested_state = input->axis_requested_state;
  return true;
}

stepper_can__srv__AxisState_Request *
stepper_can__srv__AxisState_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__srv__AxisState_Request * msg = (stepper_can__srv__AxisState_Request *)allocator.allocate(sizeof(stepper_can__srv__AxisState_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(stepper_can__srv__AxisState_Request));
  bool success = stepper_can__srv__AxisState_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
stepper_can__srv__AxisState_Request__destroy(stepper_can__srv__AxisState_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    stepper_can__srv__AxisState_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
stepper_can__srv__AxisState_Request__Sequence__init(stepper_can__srv__AxisState_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__srv__AxisState_Request * data = NULL;

  if (size) {
    data = (stepper_can__srv__AxisState_Request *)allocator.zero_allocate(size, sizeof(stepper_can__srv__AxisState_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = stepper_can__srv__AxisState_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        stepper_can__srv__AxisState_Request__fini(&data[i - 1]);
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
stepper_can__srv__AxisState_Request__Sequence__fini(stepper_can__srv__AxisState_Request__Sequence * array)
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
      stepper_can__srv__AxisState_Request__fini(&array->data[i]);
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

stepper_can__srv__AxisState_Request__Sequence *
stepper_can__srv__AxisState_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__srv__AxisState_Request__Sequence * array = (stepper_can__srv__AxisState_Request__Sequence *)allocator.allocate(sizeof(stepper_can__srv__AxisState_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = stepper_can__srv__AxisState_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
stepper_can__srv__AxisState_Request__Sequence__destroy(stepper_can__srv__AxisState_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    stepper_can__srv__AxisState_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
stepper_can__srv__AxisState_Request__Sequence__are_equal(const stepper_can__srv__AxisState_Request__Sequence * lhs, const stepper_can__srv__AxisState_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!stepper_can__srv__AxisState_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
stepper_can__srv__AxisState_Request__Sequence__copy(
  const stepper_can__srv__AxisState_Request__Sequence * input,
  stepper_can__srv__AxisState_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(stepper_can__srv__AxisState_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    stepper_can__srv__AxisState_Request * data =
      (stepper_can__srv__AxisState_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!stepper_can__srv__AxisState_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          stepper_can__srv__AxisState_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!stepper_can__srv__AxisState_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
stepper_can__srv__AxisState_Response__init(stepper_can__srv__AxisState_Response * msg)
{
  if (!msg) {
    return false;
  }
  // active_errors
  // axis_state
  // procedure_result
  return true;
}

void
stepper_can__srv__AxisState_Response__fini(stepper_can__srv__AxisState_Response * msg)
{
  if (!msg) {
    return;
  }
  // active_errors
  // axis_state
  // procedure_result
}

bool
stepper_can__srv__AxisState_Response__are_equal(const stepper_can__srv__AxisState_Response * lhs, const stepper_can__srv__AxisState_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // active_errors
  if (lhs->active_errors != rhs->active_errors) {
    return false;
  }
  // axis_state
  if (lhs->axis_state != rhs->axis_state) {
    return false;
  }
  // procedure_result
  if (lhs->procedure_result != rhs->procedure_result) {
    return false;
  }
  return true;
}

bool
stepper_can__srv__AxisState_Response__copy(
  const stepper_can__srv__AxisState_Response * input,
  stepper_can__srv__AxisState_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // active_errors
  output->active_errors = input->active_errors;
  // axis_state
  output->axis_state = input->axis_state;
  // procedure_result
  output->procedure_result = input->procedure_result;
  return true;
}

stepper_can__srv__AxisState_Response *
stepper_can__srv__AxisState_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__srv__AxisState_Response * msg = (stepper_can__srv__AxisState_Response *)allocator.allocate(sizeof(stepper_can__srv__AxisState_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(stepper_can__srv__AxisState_Response));
  bool success = stepper_can__srv__AxisState_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
stepper_can__srv__AxisState_Response__destroy(stepper_can__srv__AxisState_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    stepper_can__srv__AxisState_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
stepper_can__srv__AxisState_Response__Sequence__init(stepper_can__srv__AxisState_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__srv__AxisState_Response * data = NULL;

  if (size) {
    data = (stepper_can__srv__AxisState_Response *)allocator.zero_allocate(size, sizeof(stepper_can__srv__AxisState_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = stepper_can__srv__AxisState_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        stepper_can__srv__AxisState_Response__fini(&data[i - 1]);
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
stepper_can__srv__AxisState_Response__Sequence__fini(stepper_can__srv__AxisState_Response__Sequence * array)
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
      stepper_can__srv__AxisState_Response__fini(&array->data[i]);
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

stepper_can__srv__AxisState_Response__Sequence *
stepper_can__srv__AxisState_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  stepper_can__srv__AxisState_Response__Sequence * array = (stepper_can__srv__AxisState_Response__Sequence *)allocator.allocate(sizeof(stepper_can__srv__AxisState_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = stepper_can__srv__AxisState_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
stepper_can__srv__AxisState_Response__Sequence__destroy(stepper_can__srv__AxisState_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    stepper_can__srv__AxisState_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
stepper_can__srv__AxisState_Response__Sequence__are_equal(const stepper_can__srv__AxisState_Response__Sequence * lhs, const stepper_can__srv__AxisState_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!stepper_can__srv__AxisState_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
stepper_can__srv__AxisState_Response__Sequence__copy(
  const stepper_can__srv__AxisState_Response__Sequence * input,
  stepper_can__srv__AxisState_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(stepper_can__srv__AxisState_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    stepper_can__srv__AxisState_Response * data =
      (stepper_can__srv__AxisState_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!stepper_can__srv__AxisState_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          stepper_can__srv__AxisState_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!stepper_can__srv__AxisState_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
