// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "ares_interfaces/msg/detail/sensed_object__rosidl_typesupport_introspection_c.h"
#include "ares_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "ares_interfaces/msg/detail/sensed_object__functions.h"
#include "ares_interfaces/msg/detail/sensed_object__struct.h"


// Include directives for member types
// Member `class_name`
#include "rosidl_runtime_c/string_functions.h"
// Member `map_coords`
#include "geometry_msgs/msg/point.h"
// Member `map_coords`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ares_interfaces__msg__SensedObject__init(message_memory);
}

void ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_fini_function(void * message_memory)
{
  ares_interfaces__msg__SensedObject__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_member_array[2] = {
  {
    "class_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ares_interfaces__msg__SensedObject, class_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "map_coords",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ares_interfaces__msg__SensedObject, map_coords),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_members = {
  "ares_interfaces__msg",  // message namespace
  "SensedObject",  // message name
  2,  // number of fields
  sizeof(ares_interfaces__msg__SensedObject),
  false,  // has_any_key_member_
  ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_member_array,  // message members
  ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_init_function,  // function to initialize message memory (memory has to be allocated)
  ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_type_support_handle = {
  0,
  &ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_members,
  get_message_typesupport_handle_function,
  &ares_interfaces__msg__SensedObject__get_type_hash,
  &ares_interfaces__msg__SensedObject__get_type_description,
  &ares_interfaces__msg__SensedObject__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ares_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, msg, SensedObject)() {
  ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  if (!ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_type_support_handle.typesupport_identifier) {
    ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ares_interfaces__msg__SensedObject__rosidl_typesupport_introspection_c__SensedObject_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
