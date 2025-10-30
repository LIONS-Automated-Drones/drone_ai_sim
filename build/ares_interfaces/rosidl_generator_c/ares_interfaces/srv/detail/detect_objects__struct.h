// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/srv/detect_objects.h"


#ifndef ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__STRUCT_H_
#define ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/DetectObjects in the package ares_interfaces.
typedef struct ares_interfaces__srv__DetectObjects_Request
{
  bool trigger;
} ares_interfaces__srv__DetectObjects_Request;

// Struct for a sequence of ares_interfaces__srv__DetectObjects_Request.
typedef struct ares_interfaces__srv__DetectObjects_Request__Sequence
{
  ares_interfaces__srv__DetectObjects_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ares_interfaces__srv__DetectObjects_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'sensed_objects'
#include "ares_interfaces/msg/detail/sensed_object__struct.h"

/// Struct defined in srv/DetectObjects in the package ares_interfaces.
typedef struct ares_interfaces__srv__DetectObjects_Response
{
  ares_interfaces__msg__SensedObject__Sequence sensed_objects;
} ares_interfaces__srv__DetectObjects_Response;

// Struct for a sequence of ares_interfaces__srv__DetectObjects_Response.
typedef struct ares_interfaces__srv__DetectObjects_Response__Sequence
{
  ares_interfaces__srv__DetectObjects_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ares_interfaces__srv__DetectObjects_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  ares_interfaces__srv__DetectObjects_Event__request__MAX_SIZE = 1
};
// response
enum
{
  ares_interfaces__srv__DetectObjects_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/DetectObjects in the package ares_interfaces.
typedef struct ares_interfaces__srv__DetectObjects_Event
{
  service_msgs__msg__ServiceEventInfo info;
  ares_interfaces__srv__DetectObjects_Request__Sequence request;
  ares_interfaces__srv__DetectObjects_Response__Sequence response;
} ares_interfaces__srv__DetectObjects_Event;

// Struct for a sequence of ares_interfaces__srv__DetectObjects_Event.
typedef struct ares_interfaces__srv__DetectObjects_Event__Sequence
{
  ares_interfaces__srv__DetectObjects_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ares_interfaces__srv__DetectObjects_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__STRUCT_H_
