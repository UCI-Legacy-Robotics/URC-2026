// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice
#include "npk_sensor/srv/detail/get_soil_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
npk_sensor__srv__GetSoilData_Request__init(npk_sensor__srv__GetSoilData_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
npk_sensor__srv__GetSoilData_Request__fini(npk_sensor__srv__GetSoilData_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
npk_sensor__srv__GetSoilData_Request__are_equal(const npk_sensor__srv__GetSoilData_Request * lhs, const npk_sensor__srv__GetSoilData_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
npk_sensor__srv__GetSoilData_Request__copy(
  const npk_sensor__srv__GetSoilData_Request * input,
  npk_sensor__srv__GetSoilData_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

npk_sensor__srv__GetSoilData_Request *
npk_sensor__srv__GetSoilData_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  npk_sensor__srv__GetSoilData_Request * msg = (npk_sensor__srv__GetSoilData_Request *)allocator.allocate(sizeof(npk_sensor__srv__GetSoilData_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(npk_sensor__srv__GetSoilData_Request));
  bool success = npk_sensor__srv__GetSoilData_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
npk_sensor__srv__GetSoilData_Request__destroy(npk_sensor__srv__GetSoilData_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    npk_sensor__srv__GetSoilData_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
npk_sensor__srv__GetSoilData_Request__Sequence__init(npk_sensor__srv__GetSoilData_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  npk_sensor__srv__GetSoilData_Request * data = NULL;

  if (size) {
    data = (npk_sensor__srv__GetSoilData_Request *)allocator.zero_allocate(size, sizeof(npk_sensor__srv__GetSoilData_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = npk_sensor__srv__GetSoilData_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        npk_sensor__srv__GetSoilData_Request__fini(&data[i - 1]);
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
npk_sensor__srv__GetSoilData_Request__Sequence__fini(npk_sensor__srv__GetSoilData_Request__Sequence * array)
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
      npk_sensor__srv__GetSoilData_Request__fini(&array->data[i]);
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

npk_sensor__srv__GetSoilData_Request__Sequence *
npk_sensor__srv__GetSoilData_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  npk_sensor__srv__GetSoilData_Request__Sequence * array = (npk_sensor__srv__GetSoilData_Request__Sequence *)allocator.allocate(sizeof(npk_sensor__srv__GetSoilData_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = npk_sensor__srv__GetSoilData_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
npk_sensor__srv__GetSoilData_Request__Sequence__destroy(npk_sensor__srv__GetSoilData_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    npk_sensor__srv__GetSoilData_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
npk_sensor__srv__GetSoilData_Request__Sequence__are_equal(const npk_sensor__srv__GetSoilData_Request__Sequence * lhs, const npk_sensor__srv__GetSoilData_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!npk_sensor__srv__GetSoilData_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
npk_sensor__srv__GetSoilData_Request__Sequence__copy(
  const npk_sensor__srv__GetSoilData_Request__Sequence * input,
  npk_sensor__srv__GetSoilData_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(npk_sensor__srv__GetSoilData_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    npk_sensor__srv__GetSoilData_Request * data =
      (npk_sensor__srv__GetSoilData_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!npk_sensor__srv__GetSoilData_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          npk_sensor__srv__GetSoilData_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!npk_sensor__srv__GetSoilData_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
npk_sensor__srv__GetSoilData_Response__init(npk_sensor__srv__GetSoilData_Response * msg)
{
  if (!msg) {
    return false;
  }
  // ph
  // moisture
  // temperature
  // conductivity
  // nitrogen
  // phosphorus
  // potassium
  return true;
}

void
npk_sensor__srv__GetSoilData_Response__fini(npk_sensor__srv__GetSoilData_Response * msg)
{
  if (!msg) {
    return;
  }
  // ph
  // moisture
  // temperature
  // conductivity
  // nitrogen
  // phosphorus
  // potassium
}

bool
npk_sensor__srv__GetSoilData_Response__are_equal(const npk_sensor__srv__GetSoilData_Response * lhs, const npk_sensor__srv__GetSoilData_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // ph
  if (lhs->ph != rhs->ph) {
    return false;
  }
  // moisture
  if (lhs->moisture != rhs->moisture) {
    return false;
  }
  // temperature
  if (lhs->temperature != rhs->temperature) {
    return false;
  }
  // conductivity
  if (lhs->conductivity != rhs->conductivity) {
    return false;
  }
  // nitrogen
  if (lhs->nitrogen != rhs->nitrogen) {
    return false;
  }
  // phosphorus
  if (lhs->phosphorus != rhs->phosphorus) {
    return false;
  }
  // potassium
  if (lhs->potassium != rhs->potassium) {
    return false;
  }
  return true;
}

bool
npk_sensor__srv__GetSoilData_Response__copy(
  const npk_sensor__srv__GetSoilData_Response * input,
  npk_sensor__srv__GetSoilData_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // ph
  output->ph = input->ph;
  // moisture
  output->moisture = input->moisture;
  // temperature
  output->temperature = input->temperature;
  // conductivity
  output->conductivity = input->conductivity;
  // nitrogen
  output->nitrogen = input->nitrogen;
  // phosphorus
  output->phosphorus = input->phosphorus;
  // potassium
  output->potassium = input->potassium;
  return true;
}

npk_sensor__srv__GetSoilData_Response *
npk_sensor__srv__GetSoilData_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  npk_sensor__srv__GetSoilData_Response * msg = (npk_sensor__srv__GetSoilData_Response *)allocator.allocate(sizeof(npk_sensor__srv__GetSoilData_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(npk_sensor__srv__GetSoilData_Response));
  bool success = npk_sensor__srv__GetSoilData_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
npk_sensor__srv__GetSoilData_Response__destroy(npk_sensor__srv__GetSoilData_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    npk_sensor__srv__GetSoilData_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
npk_sensor__srv__GetSoilData_Response__Sequence__init(npk_sensor__srv__GetSoilData_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  npk_sensor__srv__GetSoilData_Response * data = NULL;

  if (size) {
    data = (npk_sensor__srv__GetSoilData_Response *)allocator.zero_allocate(size, sizeof(npk_sensor__srv__GetSoilData_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = npk_sensor__srv__GetSoilData_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        npk_sensor__srv__GetSoilData_Response__fini(&data[i - 1]);
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
npk_sensor__srv__GetSoilData_Response__Sequence__fini(npk_sensor__srv__GetSoilData_Response__Sequence * array)
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
      npk_sensor__srv__GetSoilData_Response__fini(&array->data[i]);
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

npk_sensor__srv__GetSoilData_Response__Sequence *
npk_sensor__srv__GetSoilData_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  npk_sensor__srv__GetSoilData_Response__Sequence * array = (npk_sensor__srv__GetSoilData_Response__Sequence *)allocator.allocate(sizeof(npk_sensor__srv__GetSoilData_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = npk_sensor__srv__GetSoilData_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
npk_sensor__srv__GetSoilData_Response__Sequence__destroy(npk_sensor__srv__GetSoilData_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    npk_sensor__srv__GetSoilData_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
npk_sensor__srv__GetSoilData_Response__Sequence__are_equal(const npk_sensor__srv__GetSoilData_Response__Sequence * lhs, const npk_sensor__srv__GetSoilData_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!npk_sensor__srv__GetSoilData_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
npk_sensor__srv__GetSoilData_Response__Sequence__copy(
  const npk_sensor__srv__GetSoilData_Response__Sequence * input,
  npk_sensor__srv__GetSoilData_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(npk_sensor__srv__GetSoilData_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    npk_sensor__srv__GetSoilData_Response * data =
      (npk_sensor__srv__GetSoilData_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!npk_sensor__srv__GetSoilData_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          npk_sensor__srv__GetSoilData_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!npk_sensor__srv__GetSoilData_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
