// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/msg/sensed_object.h"


#ifndef ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__STRUCT_H_
#define ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'class_name'
#include "rosidl_runtime_c/string.h"
// Member 'map_coords'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/SensedObject in the package ares_interfaces.
/**
  * SensedObject.msg
  * Represents a detected object with its 3D location in the map frame
 */
typedef struct ares_interfaces__msg__SensedObject
{
  rosidl_runtime_c__String class_name;
  geometry_msgs__msg__Point map_coords;
} ares_interfaces__msg__SensedObject;

// Struct for a sequence of ares_interfaces__msg__SensedObject.
typedef struct ares_interfaces__msg__SensedObject__Sequence
{
  ares_interfaces__msg__SensedObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ares_interfaces__msg__SensedObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__STRUCT_H_
