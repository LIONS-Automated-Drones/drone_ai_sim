// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "ares_interfaces/srv/detail/detect_objects__rosidl_typesupport_introspection_c.h"
#include "ares_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "ares_interfaces/srv/detail/detect_objects__functions.h"
#include "ares_interfaces/srv/detail/detect_objects__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ares_interfaces__srv__DetectObjects_Request__init(message_memory);
}

void ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_fini_function(void * message_memory)
{
  ares_interfaces__srv__DetectObjects_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_member_array[1] = {
  {
    "trigger",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ares_interfaces__srv__DetectObjects_Request, trigger),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_members = {
  "ares_interfaces__srv",  // message namespace
  "DetectObjects_Request",  // message name
  1,  // number of fields
  sizeof(ares_interfaces__srv__DetectObjects_Request),
  false,  // has_any_key_member_
  ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_member_array,  // message members
  ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_type_support_handle = {
  0,
  &ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_members,
  get_message_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Request__get_type_hash,
  &ares_interfaces__srv__DetectObjects_Request__get_type_description,
  &ares_interfaces__srv__DetectObjects_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ares_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Request)() {
  if (!ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_type_support_handle.typesupport_identifier) {
    ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__rosidl_typesupport_introspection_c.h"
// already included above
// #include "ares_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__functions.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__struct.h"


// Include directives for member types
// Member `sensed_objects`
#include "ares_interfaces/msg/sensed_object.h"
// Member `sensed_objects`
#include "ares_interfaces/msg/detail/sensed_object__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ares_interfaces__srv__DetectObjects_Response__init(message_memory);
}

void ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_fini_function(void * message_memory)
{
  ares_interfaces__srv__DetectObjects_Response__fini(message_memory);
}

size_t ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__size_function__DetectObjects_Response__sensed_objects(
  const void * untyped_member)
{
  const ares_interfaces__msg__SensedObject__Sequence * member =
    (const ares_interfaces__msg__SensedObject__Sequence *)(untyped_member);
  return member->size;
}

const void * ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Response__sensed_objects(
  const void * untyped_member, size_t index)
{
  const ares_interfaces__msg__SensedObject__Sequence * member =
    (const ares_interfaces__msg__SensedObject__Sequence *)(untyped_member);
  return &member->data[index];
}

void * ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__get_function__DetectObjects_Response__sensed_objects(
  void * untyped_member, size_t index)
{
  ares_interfaces__msg__SensedObject__Sequence * member =
    (ares_interfaces__msg__SensedObject__Sequence *)(untyped_member);
  return &member->data[index];
}

void ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__fetch_function__DetectObjects_Response__sensed_objects(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const ares_interfaces__msg__SensedObject * item =
    ((const ares_interfaces__msg__SensedObject *)
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Response__sensed_objects(untyped_member, index));
  ares_interfaces__msg__SensedObject * value =
    (ares_interfaces__msg__SensedObject *)(untyped_value);
  *value = *item;
}

void ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__assign_function__DetectObjects_Response__sensed_objects(
  void * untyped_member, size_t index, const void * untyped_value)
{
  ares_interfaces__msg__SensedObject * item =
    ((ares_interfaces__msg__SensedObject *)
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__get_function__DetectObjects_Response__sensed_objects(untyped_member, index));
  const ares_interfaces__msg__SensedObject * value =
    (const ares_interfaces__msg__SensedObject *)(untyped_value);
  *item = *value;
}

bool ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__resize_function__DetectObjects_Response__sensed_objects(
  void * untyped_member, size_t size)
{
  ares_interfaces__msg__SensedObject__Sequence * member =
    (ares_interfaces__msg__SensedObject__Sequence *)(untyped_member);
  ares_interfaces__msg__SensedObject__Sequence__fini(member);
  return ares_interfaces__msg__SensedObject__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_member_array[1] = {
  {
    "sensed_objects",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ares_interfaces__srv__DetectObjects_Response, sensed_objects),  // bytes offset in struct
    NULL,  // default value
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__size_function__DetectObjects_Response__sensed_objects,  // size() function pointer
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Response__sensed_objects,  // get_const(index) function pointer
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__get_function__DetectObjects_Response__sensed_objects,  // get(index) function pointer
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__fetch_function__DetectObjects_Response__sensed_objects,  // fetch(index, &value) function pointer
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__assign_function__DetectObjects_Response__sensed_objects,  // assign(index, value) function pointer
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__resize_function__DetectObjects_Response__sensed_objects  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_members = {
  "ares_interfaces__srv",  // message namespace
  "DetectObjects_Response",  // message name
  1,  // number of fields
  sizeof(ares_interfaces__srv__DetectObjects_Response),
  false,  // has_any_key_member_
  ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_member_array,  // message members
  ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle = {
  0,
  &ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_members,
  get_message_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Response__get_type_hash,
  &ares_interfaces__srv__DetectObjects_Response__get_type_description,
  &ares_interfaces__srv__DetectObjects_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ares_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Response)() {
  ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, msg, SensedObject)();
  if (!ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle.typesupport_identifier) {
    ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__rosidl_typesupport_introspection_c.h"
// already included above
// #include "ares_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__functions.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "ares_interfaces/srv/detect_objects.h"
// Member `request`
// Member `response`
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  ares_interfaces__srv__DetectObjects_Event__init(message_memory);
}

void ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_fini_function(void * message_memory)
{
  ares_interfaces__srv__DetectObjects_Event__fini(message_memory);
}

size_t ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__size_function__DetectObjects_Event__request(
  const void * untyped_member)
{
  const ares_interfaces__srv__DetectObjects_Request__Sequence * member =
    (const ares_interfaces__srv__DetectObjects_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Event__request(
  const void * untyped_member, size_t index)
{
  const ares_interfaces__srv__DetectObjects_Request__Sequence * member =
    (const ares_interfaces__srv__DetectObjects_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_function__DetectObjects_Event__request(
  void * untyped_member, size_t index)
{
  ares_interfaces__srv__DetectObjects_Request__Sequence * member =
    (ares_interfaces__srv__DetectObjects_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__fetch_function__DetectObjects_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const ares_interfaces__srv__DetectObjects_Request * item =
    ((const ares_interfaces__srv__DetectObjects_Request *)
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Event__request(untyped_member, index));
  ares_interfaces__srv__DetectObjects_Request * value =
    (ares_interfaces__srv__DetectObjects_Request *)(untyped_value);
  *value = *item;
}

void ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__assign_function__DetectObjects_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  ares_interfaces__srv__DetectObjects_Request * item =
    ((ares_interfaces__srv__DetectObjects_Request *)
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_function__DetectObjects_Event__request(untyped_member, index));
  const ares_interfaces__srv__DetectObjects_Request * value =
    (const ares_interfaces__srv__DetectObjects_Request *)(untyped_value);
  *item = *value;
}

bool ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__resize_function__DetectObjects_Event__request(
  void * untyped_member, size_t size)
{
  ares_interfaces__srv__DetectObjects_Request__Sequence * member =
    (ares_interfaces__srv__DetectObjects_Request__Sequence *)(untyped_member);
  ares_interfaces__srv__DetectObjects_Request__Sequence__fini(member);
  return ares_interfaces__srv__DetectObjects_Request__Sequence__init(member, size);
}

size_t ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__size_function__DetectObjects_Event__response(
  const void * untyped_member)
{
  const ares_interfaces__srv__DetectObjects_Response__Sequence * member =
    (const ares_interfaces__srv__DetectObjects_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Event__response(
  const void * untyped_member, size_t index)
{
  const ares_interfaces__srv__DetectObjects_Response__Sequence * member =
    (const ares_interfaces__srv__DetectObjects_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_function__DetectObjects_Event__response(
  void * untyped_member, size_t index)
{
  ares_interfaces__srv__DetectObjects_Response__Sequence * member =
    (ares_interfaces__srv__DetectObjects_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__fetch_function__DetectObjects_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const ares_interfaces__srv__DetectObjects_Response * item =
    ((const ares_interfaces__srv__DetectObjects_Response *)
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Event__response(untyped_member, index));
  ares_interfaces__srv__DetectObjects_Response * value =
    (ares_interfaces__srv__DetectObjects_Response *)(untyped_value);
  *value = *item;
}

void ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__assign_function__DetectObjects_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  ares_interfaces__srv__DetectObjects_Response * item =
    ((ares_interfaces__srv__DetectObjects_Response *)
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_function__DetectObjects_Event__response(untyped_member, index));
  const ares_interfaces__srv__DetectObjects_Response * value =
    (const ares_interfaces__srv__DetectObjects_Response *)(untyped_value);
  *item = *value;
}

bool ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__resize_function__DetectObjects_Event__response(
  void * untyped_member, size_t size)
{
  ares_interfaces__srv__DetectObjects_Response__Sequence * member =
    (ares_interfaces__srv__DetectObjects_Response__Sequence *)(untyped_member);
  ares_interfaces__srv__DetectObjects_Response__Sequence__fini(member);
  return ares_interfaces__srv__DetectObjects_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(ares_interfaces__srv__DetectObjects_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(ares_interfaces__srv__DetectObjects_Event, request),  // bytes offset in struct
    NULL,  // default value
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__size_function__DetectObjects_Event__request,  // size() function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Event__request,  // get_const(index) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_function__DetectObjects_Event__request,  // get(index) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__fetch_function__DetectObjects_Event__request,  // fetch(index, &value) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__assign_function__DetectObjects_Event__request,  // assign(index, value) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__resize_function__DetectObjects_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(ares_interfaces__srv__DetectObjects_Event, response),  // bytes offset in struct
    NULL,  // default value
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__size_function__DetectObjects_Event__response,  // size() function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_const_function__DetectObjects_Event__response,  // get_const(index) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__get_function__DetectObjects_Event__response,  // get(index) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__fetch_function__DetectObjects_Event__response,  // fetch(index, &value) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__assign_function__DetectObjects_Event__response,  // assign(index, value) function pointer
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__resize_function__DetectObjects_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_members = {
  "ares_interfaces__srv",  // message namespace
  "DetectObjects_Event",  // message name
  3,  // number of fields
  sizeof(ares_interfaces__srv__DetectObjects_Event),
  false,  // has_any_key_member_
  ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_member_array,  // message members
  ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_type_support_handle = {
  0,
  &ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_members,
  get_message_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Event__get_type_hash,
  &ares_interfaces__srv__DetectObjects_Event__get_type_description,
  &ares_interfaces__srv__DetectObjects_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ares_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Event)() {
  ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Request)();
  ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Response)();
  if (!ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_type_support_handle.typesupport_identifier) {
    ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "ares_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_members = {
  "ares_interfaces__srv",  // service namespace
  "DetectObjects",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_Request_message_type_support_handle,
  NULL,  // response message
  // ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle
  NULL  // event_message
  // ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle
};


static rosidl_service_type_support_t ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_type_support_handle = {
  0,
  &ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_members,
  get_service_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Request__rosidl_typesupport_introspection_c__DetectObjects_Request_message_type_support_handle,
  &ares_interfaces__srv__DetectObjects_Response__rosidl_typesupport_introspection_c__DetectObjects_Response_message_type_support_handle,
  &ares_interfaces__srv__DetectObjects_Event__rosidl_typesupport_introspection_c__DetectObjects_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    ares_interfaces,
    srv,
    DetectObjects
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    ares_interfaces,
    srv,
    DetectObjects
  ),
  &ares_interfaces__srv__DetectObjects__get_type_hash,
  &ares_interfaces__srv__DetectObjects__get_type_description,
  &ares_interfaces__srv__DetectObjects__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_ares_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects)(void) {
  if (!ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_type_support_handle.typesupport_identifier) {
    ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, ares_interfaces, srv, DetectObjects_Event)()->data;
  }

  return &ares_interfaces__srv__detail__detect_objects__rosidl_typesupport_introspection_c__DetectObjects_service_type_support_handle;
}
