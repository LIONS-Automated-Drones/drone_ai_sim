// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice
#ifndef ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "ares_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "ares_interfaces/msg/detail/sensed_object__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
bool cdr_serialize_ares_interfaces__msg__SensedObject(
  const ares_interfaces__msg__SensedObject * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
bool cdr_deserialize_ares_interfaces__msg__SensedObject(
  eprosima::fastcdr::Cdr &,
  ares_interfaces__msg__SensedObject * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
size_t get_serialized_size_ares_interfaces__msg__SensedObject(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
size_t max_serialized_size_ares_interfaces__msg__SensedObject(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
bool cdr_serialize_key_ares_interfaces__msg__SensedObject(
  const ares_interfaces__msg__SensedObject * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
size_t get_serialized_size_key_ares_interfaces__msg__SensedObject(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
size_t max_serialized_size_key_ares_interfaces__msg__SensedObject(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ares_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ares_interfaces, msg, SensedObject)();

#ifdef __cplusplus
}
#endif

#endif  // ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
