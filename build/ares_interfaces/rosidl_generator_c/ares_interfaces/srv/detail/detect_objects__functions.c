// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice
#include "ares_interfaces/srv/detail/detect_objects__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
ares_interfaces__srv__DetectObjects_Request__init(ares_interfaces__srv__DetectObjects_Request * msg)
{
  if (!msg) {
    return false;
  }
  // trigger
  return true;
}

void
ares_interfaces__srv__DetectObjects_Request__fini(ares_interfaces__srv__DetectObjects_Request * msg)
{
  if (!msg) {
    return;
  }
  // trigger
}

bool
ares_interfaces__srv__DetectObjects_Request__are_equal(const ares_interfaces__srv__DetectObjects_Request * lhs, const ares_interfaces__srv__DetectObjects_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // trigger
  if (lhs->trigger != rhs->trigger) {
    return false;
  }
  return true;
}

bool
ares_interfaces__srv__DetectObjects_Request__copy(
  const ares_interfaces__srv__DetectObjects_Request * input,
  ares_interfaces__srv__DetectObjects_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // trigger
  output->trigger = input->trigger;
  return true;
}

ares_interfaces__srv__DetectObjects_Request *
ares_interfaces__srv__DetectObjects_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Request * msg = (ares_interfaces__srv__DetectObjects_Request *)allocator.allocate(sizeof(ares_interfaces__srv__DetectObjects_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ares_interfaces__srv__DetectObjects_Request));
  bool success = ares_interfaces__srv__DetectObjects_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ares_interfaces__srv__DetectObjects_Request__destroy(ares_interfaces__srv__DetectObjects_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ares_interfaces__srv__DetectObjects_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ares_interfaces__srv__DetectObjects_Request__Sequence__init(ares_interfaces__srv__DetectObjects_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Request * data = NULL;

  if (size) {
    data = (ares_interfaces__srv__DetectObjects_Request *)allocator.zero_allocate(size, sizeof(ares_interfaces__srv__DetectObjects_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ares_interfaces__srv__DetectObjects_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ares_interfaces__srv__DetectObjects_Request__fini(&data[i - 1]);
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
ares_interfaces__srv__DetectObjects_Request__Sequence__fini(ares_interfaces__srv__DetectObjects_Request__Sequence * array)
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
      ares_interfaces__srv__DetectObjects_Request__fini(&array->data[i]);
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

ares_interfaces__srv__DetectObjects_Request__Sequence *
ares_interfaces__srv__DetectObjects_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Request__Sequence * array = (ares_interfaces__srv__DetectObjects_Request__Sequence *)allocator.allocate(sizeof(ares_interfaces__srv__DetectObjects_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ares_interfaces__srv__DetectObjects_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ares_interfaces__srv__DetectObjects_Request__Sequence__destroy(ares_interfaces__srv__DetectObjects_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ares_interfaces__srv__DetectObjects_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ares_interfaces__srv__DetectObjects_Request__Sequence__are_equal(const ares_interfaces__srv__DetectObjects_Request__Sequence * lhs, const ares_interfaces__srv__DetectObjects_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ares_interfaces__srv__DetectObjects_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ares_interfaces__srv__DetectObjects_Request__Sequence__copy(
  const ares_interfaces__srv__DetectObjects_Request__Sequence * input,
  ares_interfaces__srv__DetectObjects_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ares_interfaces__srv__DetectObjects_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ares_interfaces__srv__DetectObjects_Request * data =
      (ares_interfaces__srv__DetectObjects_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ares_interfaces__srv__DetectObjects_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ares_interfaces__srv__DetectObjects_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ares_interfaces__srv__DetectObjects_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `sensed_objects`
#include "ares_interfaces/msg/detail/sensed_object__functions.h"

bool
ares_interfaces__srv__DetectObjects_Response__init(ares_interfaces__srv__DetectObjects_Response * msg)
{
  if (!msg) {
    return false;
  }
  // sensed_objects
  if (!ares_interfaces__msg__SensedObject__Sequence__init(&msg->sensed_objects, 0)) {
    ares_interfaces__srv__DetectObjects_Response__fini(msg);
    return false;
  }
  return true;
}

void
ares_interfaces__srv__DetectObjects_Response__fini(ares_interfaces__srv__DetectObjects_Response * msg)
{
  if (!msg) {
    return;
  }
  // sensed_objects
  ares_interfaces__msg__SensedObject__Sequence__fini(&msg->sensed_objects);
}

bool
ares_interfaces__srv__DetectObjects_Response__are_equal(const ares_interfaces__srv__DetectObjects_Response * lhs, const ares_interfaces__srv__DetectObjects_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // sensed_objects
  if (!ares_interfaces__msg__SensedObject__Sequence__are_equal(
      &(lhs->sensed_objects), &(rhs->sensed_objects)))
  {
    return false;
  }
  return true;
}

bool
ares_interfaces__srv__DetectObjects_Response__copy(
  const ares_interfaces__srv__DetectObjects_Response * input,
  ares_interfaces__srv__DetectObjects_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // sensed_objects
  if (!ares_interfaces__msg__SensedObject__Sequence__copy(
      &(input->sensed_objects), &(output->sensed_objects)))
  {
    return false;
  }
  return true;
}

ares_interfaces__srv__DetectObjects_Response *
ares_interfaces__srv__DetectObjects_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Response * msg = (ares_interfaces__srv__DetectObjects_Response *)allocator.allocate(sizeof(ares_interfaces__srv__DetectObjects_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ares_interfaces__srv__DetectObjects_Response));
  bool success = ares_interfaces__srv__DetectObjects_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ares_interfaces__srv__DetectObjects_Response__destroy(ares_interfaces__srv__DetectObjects_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ares_interfaces__srv__DetectObjects_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ares_interfaces__srv__DetectObjects_Response__Sequence__init(ares_interfaces__srv__DetectObjects_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Response * data = NULL;

  if (size) {
    data = (ares_interfaces__srv__DetectObjects_Response *)allocator.zero_allocate(size, sizeof(ares_interfaces__srv__DetectObjects_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ares_interfaces__srv__DetectObjects_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ares_interfaces__srv__DetectObjects_Response__fini(&data[i - 1]);
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
ares_interfaces__srv__DetectObjects_Response__Sequence__fini(ares_interfaces__srv__DetectObjects_Response__Sequence * array)
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
      ares_interfaces__srv__DetectObjects_Response__fini(&array->data[i]);
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

ares_interfaces__srv__DetectObjects_Response__Sequence *
ares_interfaces__srv__DetectObjects_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Response__Sequence * array = (ares_interfaces__srv__DetectObjects_Response__Sequence *)allocator.allocate(sizeof(ares_interfaces__srv__DetectObjects_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ares_interfaces__srv__DetectObjects_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ares_interfaces__srv__DetectObjects_Response__Sequence__destroy(ares_interfaces__srv__DetectObjects_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ares_interfaces__srv__DetectObjects_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ares_interfaces__srv__DetectObjects_Response__Sequence__are_equal(const ares_interfaces__srv__DetectObjects_Response__Sequence * lhs, const ares_interfaces__srv__DetectObjects_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ares_interfaces__srv__DetectObjects_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ares_interfaces__srv__DetectObjects_Response__Sequence__copy(
  const ares_interfaces__srv__DetectObjects_Response__Sequence * input,
  ares_interfaces__srv__DetectObjects_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ares_interfaces__srv__DetectObjects_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ares_interfaces__srv__DetectObjects_Response * data =
      (ares_interfaces__srv__DetectObjects_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ares_interfaces__srv__DetectObjects_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ares_interfaces__srv__DetectObjects_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ares_interfaces__srv__DetectObjects_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__functions.h"

bool
ares_interfaces__srv__DetectObjects_Event__init(ares_interfaces__srv__DetectObjects_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    ares_interfaces__srv__DetectObjects_Event__fini(msg);
    return false;
  }
  // request
  if (!ares_interfaces__srv__DetectObjects_Request__Sequence__init(&msg->request, 0)) {
    ares_interfaces__srv__DetectObjects_Event__fini(msg);
    return false;
  }
  // response
  if (!ares_interfaces__srv__DetectObjects_Response__Sequence__init(&msg->response, 0)) {
    ares_interfaces__srv__DetectObjects_Event__fini(msg);
    return false;
  }
  return true;
}

void
ares_interfaces__srv__DetectObjects_Event__fini(ares_interfaces__srv__DetectObjects_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  ares_interfaces__srv__DetectObjects_Request__Sequence__fini(&msg->request);
  // response
  ares_interfaces__srv__DetectObjects_Response__Sequence__fini(&msg->response);
}

bool
ares_interfaces__srv__DetectObjects_Event__are_equal(const ares_interfaces__srv__DetectObjects_Event * lhs, const ares_interfaces__srv__DetectObjects_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!ares_interfaces__srv__DetectObjects_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!ares_interfaces__srv__DetectObjects_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
ares_interfaces__srv__DetectObjects_Event__copy(
  const ares_interfaces__srv__DetectObjects_Event * input,
  ares_interfaces__srv__DetectObjects_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!ares_interfaces__srv__DetectObjects_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!ares_interfaces__srv__DetectObjects_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

ares_interfaces__srv__DetectObjects_Event *
ares_interfaces__srv__DetectObjects_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Event * msg = (ares_interfaces__srv__DetectObjects_Event *)allocator.allocate(sizeof(ares_interfaces__srv__DetectObjects_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ares_interfaces__srv__DetectObjects_Event));
  bool success = ares_interfaces__srv__DetectObjects_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ares_interfaces__srv__DetectObjects_Event__destroy(ares_interfaces__srv__DetectObjects_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ares_interfaces__srv__DetectObjects_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ares_interfaces__srv__DetectObjects_Event__Sequence__init(ares_interfaces__srv__DetectObjects_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Event * data = NULL;

  if (size) {
    data = (ares_interfaces__srv__DetectObjects_Event *)allocator.zero_allocate(size, sizeof(ares_interfaces__srv__DetectObjects_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ares_interfaces__srv__DetectObjects_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ares_interfaces__srv__DetectObjects_Event__fini(&data[i - 1]);
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
ares_interfaces__srv__DetectObjects_Event__Sequence__fini(ares_interfaces__srv__DetectObjects_Event__Sequence * array)
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
      ares_interfaces__srv__DetectObjects_Event__fini(&array->data[i]);
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

ares_interfaces__srv__DetectObjects_Event__Sequence *
ares_interfaces__srv__DetectObjects_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ares_interfaces__srv__DetectObjects_Event__Sequence * array = (ares_interfaces__srv__DetectObjects_Event__Sequence *)allocator.allocate(sizeof(ares_interfaces__srv__DetectObjects_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ares_interfaces__srv__DetectObjects_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ares_interfaces__srv__DetectObjects_Event__Sequence__destroy(ares_interfaces__srv__DetectObjects_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ares_interfaces__srv__DetectObjects_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ares_interfaces__srv__DetectObjects_Event__Sequence__are_equal(const ares_interfaces__srv__DetectObjects_Event__Sequence * lhs, const ares_interfaces__srv__DetectObjects_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ares_interfaces__srv__DetectObjects_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ares_interfaces__srv__DetectObjects_Event__Sequence__copy(
  const ares_interfaces__srv__DetectObjects_Event__Sequence * input,
  ares_interfaces__srv__DetectObjects_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ares_interfaces__srv__DetectObjects_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ares_interfaces__srv__DetectObjects_Event * data =
      (ares_interfaces__srv__DetectObjects_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ares_interfaces__srv__DetectObjects_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ares_interfaces__srv__DetectObjects_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ares_interfaces__srv__DetectObjects_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
