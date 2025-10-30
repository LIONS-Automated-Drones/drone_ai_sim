// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

#include "ares_interfaces/msg/detail/sensed_object__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_type_hash_t *
ares_interfaces__msg__SensedObject__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd0, 0x43, 0xbf, 0xcc, 0x5e, 0xfc, 0x33, 0x6e,
      0x51, 0x65, 0x45, 0x09, 0xf7, 0xfc, 0x2c, 0xf3,
      0x66, 0x73, 0xc6, 0x9e, 0x24, 0x51, 0xf8, 0xc6,
      0x59, 0x55, 0xe8, 0xf1, 0x78, 0xee, 0x85, 0x72,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "geometry_msgs/msg/detail/point__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t geometry_msgs__msg__Point__EXPECTED_HASH = {1, {
    0x69, 0x63, 0x08, 0x48, 0x42, 0xa9, 0xb0, 0x44,
    0x94, 0xd6, 0xb2, 0x94, 0x1d, 0x11, 0x44, 0x47,
    0x08, 0xd8, 0x92, 0xda, 0x2f, 0x4b, 0x09, 0x84,
    0x3b, 0x9c, 0x43, 0xf4, 0x2a, 0x7f, 0x68, 0x81,
  }};
#endif

static char ares_interfaces__msg__SensedObject__TYPE_NAME[] = "ares_interfaces/msg/SensedObject";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";

// Define type names, field names, and default values
static char ares_interfaces__msg__SensedObject__FIELD_NAME__class_name[] = "class_name";
static char ares_interfaces__msg__SensedObject__FIELD_NAME__map_coords[] = "map_coords";

static rosidl_runtime_c__type_description__Field ares_interfaces__msg__SensedObject__FIELDS[] = {
  {
    {ares_interfaces__msg__SensedObject__FIELD_NAME__class_name, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__msg__SensedObject__FIELD_NAME__map_coords, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription ares_interfaces__msg__SensedObject__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ares_interfaces__msg__SensedObject__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ares_interfaces__msg__SensedObject__TYPE_NAME, 32, 32},
      {ares_interfaces__msg__SensedObject__FIELDS, 2, 2},
    },
    {ares_interfaces__msg__SensedObject__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# SensedObject.msg\n"
  "# Represents a detected object with its 3D location in the map frame\n"
  "\n"
  "string class_name\n"
  "geometry_msgs/Point map_coords\n"
  "";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
ares_interfaces__msg__SensedObject__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ares_interfaces__msg__SensedObject__TYPE_NAME, 32, 32},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 139, 139},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ares_interfaces__msg__SensedObject__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ares_interfaces__msg__SensedObject__get_individual_type_description_source(NULL),
    sources[1] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
