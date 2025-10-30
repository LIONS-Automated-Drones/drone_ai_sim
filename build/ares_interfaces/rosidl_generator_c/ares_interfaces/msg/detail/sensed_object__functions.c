// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice
#include "ares_interfaces/msg/detail/sensed_object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `class_name`
#include "rosidl_runtime_c/string_functions.h"
// Member `map_coords`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
ares_interfaces__msg__SensedObject__init(ares_interfaces__msg__SensedObject * msg)
{
  if (!msg) {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__init(&msg->class_name)) {
    ares_interfaces__msg__SensedObject__fini(msg);
    return false;
  }
  // map_coords
  if (!geometry_msgs__msg__Point__init(&msg->map_coords)) {
    ares_interfaces__msg__SensedObject__fini(msg);
    return false;
  }
  return true;
}

void
ares_interfaces__msg__SensedObject__fini(ares_interfaces__msg__SensedObject * msg)
{
  if (!msg) {
    return;
  }
  // class_name
  rosidl_runtime_c__String__fini(&msg->class_name);
  // map_coords
  geometry_msgs__msg__Point__fini(&msg->map_coords);
}

bool
ares_interfaces__msg__SensedObject__are_equal(const ares_interfaces__msg__SensedObject * lhs, const ares_interfaces__msg__SensedObject * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->class_name), &(rhs->class_name)))
  {
    return false;
  }
  // map_coords
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->map_coords), &(rhs->map_coords)))
  {
    return false;
  }
  return true;
}

bool
ares_interfaces__msg__SensedObject__copy(
  const ares_interfaces__msg__SensedObject * input,
  ares_interfaces__msg__SensedObject * output)
{
  if (!input || !output) {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__copy(
      &(input->class_name), &(output->class_name)))
  {
    return false;
  }
  // map_coords
  if (!geometry_msgs__msg__Point__copy(
      &(input->map_coords), &(output->map_coords)))
  {
    return false;
  }
  return true;
}

ares_interfaces__msg__SensedObject *
ares_interfaces__msg__SensedObject__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__msg__SensedObject * msg = (ares_interfaces__msg__SensedObject *)allocator.allocate(sizeof(ares_interfaces__msg__SensedObject), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ares_interfaces__msg__SensedObject));
  bool success = ares_interfaces__msg__SensedObject__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ares_interfaces__msg__SensedObject__destroy(ares_interfaces__msg__SensedObject * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ares_interfaces__msg__SensedObject__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ares_interfaces__msg__SensedObject__Sequence__init(ares_interfaces__msg__SensedObject__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__msg__SensedObject * data = NULL;

  if (size) {
    data = (ares_interfaces__msg__SensedObject *)allocator.zero_allocate(size, sizeof(ares_interfaces__msg__SensedObject), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ares_interfaces__msg__SensedObject__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ares_interfaces__msg__SensedObject__fini(&data[i - 1]);
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
ares_interfaces__msg__SensedObject__Sequence__fini(ares_interfaces__msg__SensedObject__Sequence * array)
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
      ares_interfaces__msg__SensedObject__fini(&array->data[i]);
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

ares_interfaces__msg__SensedObject__Sequence *
ares_interfaces__msg__SensedObject__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__msg__SensedObject__Sequence * array = (ares_interfaces__msg__SensedObject__Sequence *)allocator.allocate(sizeof(ares_interfaces__msg__SensedObject__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ares_interfaces__msg__SensedObject__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ares_interfaces__msg__SensedObject__Sequence__destroy(ares_interfaces__msg__SensedObject__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ares_interfaces__msg__SensedObject__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ares_interfaces__msg__SensedObject__Sequence__are_equal(const ares_interfaces__msg__SensedObject__Sequence * lhs, const ares_interfaces__msg__SensedObject__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ares_interfaces__msg__SensedObject__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ares_interfaces__msg__SensedObject__Sequence__copy(
  const ares_interfaces__msg__SensedObject__Sequence * input,
  ares_interfaces__msg__SensedObject__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ares_interfaces__msg__SensedObject);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ares_interfaces__msg__SensedObject * data =
      (ares_interfaces__msg__SensedObject *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ares_interfaces__msg__SensedObject__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ares_interfaces__msg__SensedObject__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ares_interfaces__msg__SensedObject__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
