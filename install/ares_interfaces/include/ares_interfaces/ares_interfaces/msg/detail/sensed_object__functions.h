// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/msg/sensed_object.h"


#ifndef ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__FUNCTIONS_H_
#define ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "ares_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "ares_interfaces/msg/detail/sensed_object__struct.h"

/// Initialize msg/SensedObject message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * ares_interfaces__msg__SensedObject
 * )) before or use
 * ares_interfaces__msg__SensedObject__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
bool
ares_interfaces__msg__SensedObject__init(ares_interfaces__msg__SensedObject * msg);

/// Finalize msg/SensedObject message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
void
ares_interfaces__msg__SensedObject__fini(ares_interfaces__msg__SensedObject * msg);

/// Create msg/SensedObject message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * ares_interfaces__msg__SensedObject__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
ares_interfaces__msg__SensedObject *
ares_interfaces__msg__SensedObject__create(void);

/// Destroy msg/SensedObject message.
/**
 * It calls
 * ares_interfaces__msg__SensedObject__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
void
ares_interfaces__msg__SensedObject__destroy(ares_interfaces__msg__SensedObject * msg);

/// Check for msg/SensedObject message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
bool
ares_interfaces__msg__SensedObject__are_equal(const ares_interfaces__msg__SensedObject * lhs, const ares_interfaces__msg__SensedObject * rhs);

/// Copy a msg/SensedObject message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
bool
ares_interfaces__msg__SensedObject__copy(
  const ares_interfaces__msg__SensedObject * input,
  ares_interfaces__msg__SensedObject * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_type_hash_t *
ares_interfaces__msg__SensedObject__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
ares_interfaces__msg__SensedObject__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_runtime_c__type_description__TypeSource *
ares_interfaces__msg__SensedObject__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
ares_interfaces__msg__SensedObject__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/SensedObject messages.
/**
 * It allocates the memory for the number of elements and calls
 * ares_interfaces__msg__SensedObject__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
bool
ares_interfaces__msg__SensedObject__Sequence__init(ares_interfaces__msg__SensedObject__Sequence * array, size_t size);

/// Finalize array of msg/SensedObject messages.
/**
 * It calls
 * ares_interfaces__msg__SensedObject__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
void
ares_interfaces__msg__SensedObject__Sequence__fini(ares_interfaces__msg__SensedObject__Sequence * array);

/// Create array of msg/SensedObject messages.
/**
 * It allocates the memory for the array and calls
 * ares_interfaces__msg__SensedObject__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
ares_interfaces__msg__SensedObject__Sequence *
ares_interfaces__msg__SensedObject__Sequence__create(size_t size);

/// Destroy array of msg/SensedObject messages.
/**
 * It calls
 * ares_interfaces__msg__SensedObject__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
void
ares_interfaces__msg__SensedObject__Sequence__destroy(ares_interfaces__msg__SensedObject__Sequence * array);

/// Check for msg/SensedObject message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
bool
ares_interfaces__msg__SensedObject__Sequence__are_equal(const ares_interfaces__msg__SensedObject__Sequence * lhs, const ares_interfaces__msg__SensedObject__Sequence * rhs);

/// Copy an array of msg/SensedObject messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
bool
ares_interfaces__msg__SensedObject__Sequence__copy(
  const ares_interfaces__msg__SensedObject__Sequence * input,
  ares_interfaces__msg__SensedObject__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__FUNCTIONS_H_
