// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice

#include "ares_interfaces/srv/detail/detect_objects__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_type_hash_t *
ares_interfaces__srv__DetectObjects__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x01, 0xc0, 0x88, 0xf4, 0xdb, 0xa0, 0x99, 0xf6,
      0x81, 0xb1, 0xe9, 0xd9, 0x5e, 0xc9, 0x54, 0x88,
      0xc1, 0xe3, 0x19, 0x41, 0x0e, 0x7d, 0x08, 0x97,
      0x2e, 0xe1, 0x83, 0xd9, 0xe8, 0x30, 0xed, 0x7a,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_type_hash_t *
ares_interfaces__srv__DetectObjects_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xfa, 0xfe, 0x52, 0xe4, 0x74, 0xee, 0x33, 0xbf,
      0x28, 0x25, 0x86, 0x8e, 0x70, 0x40, 0x86, 0xd5,
      0xec, 0x79, 0x5e, 0x35, 0xff, 0xb8, 0xa2, 0x61,
      0xd1, 0xc1, 0x6e, 0xa7, 0xc4, 0xd0, 0x9b, 0xc9,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_type_hash_t *
ares_interfaces__srv__DetectObjects_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xcc, 0x22, 0x7e, 0xe0, 0xea, 0xce, 0x4b, 0x8f,
      0xb8, 0xc8, 0xd1, 0xba, 0xae, 0xf9, 0x41, 0x79,
      0x1c, 0xad, 0x97, 0xd1, 0x3a, 0xb8, 0xfe, 0xc3,
      0x01, 0x32, 0x57, 0x59, 0xb9, 0xed, 0xb2, 0x03,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_ares_interfaces
const rosidl_type_hash_t *
ares_interfaces__srv__DetectObjects_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xbf, 0xef, 0x08, 0xe1, 0x4c, 0x90, 0x74, 0x83,
      0x70, 0x15, 0x7f, 0x68, 0x51, 0x83, 0xfd, 0x7b,
      0xa8, 0x37, 0xa2, 0xc1, 0xc6, 0xce, 0xf4, 0x4a,
      0x5e, 0x34, 0x8f, 0x5c, 0xc8, 0x33, 0x51, 0x8e,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "ares_interfaces/msg/detail/sensed_object__functions.h"
#include "service_msgs/msg/detail/service_event_info__functions.h"
#include "geometry_msgs/msg/detail/point__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t ares_interfaces__msg__SensedObject__EXPECTED_HASH = {1, {
    0xd0, 0x43, 0xbf, 0xcc, 0x5e, 0xfc, 0x33, 0x6e,
    0x51, 0x65, 0x45, 0x09, 0xf7, 0xfc, 0x2c, 0xf3,
    0x66, 0x73, 0xc6, 0x9e, 0x24, 0x51, 0xf8, 0xc6,
    0x59, 0x55, 0xe8, 0xf1, 0x78, 0xee, 0x85, 0x72,
  }};
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Point__EXPECTED_HASH = {1, {
    0x69, 0x63, 0x08, 0x48, 0x42, 0xa9, 0xb0, 0x44,
    0x94, 0xd6, 0xb2, 0x94, 0x1d, 0x11, 0x44, 0x47,
    0x08, 0xd8, 0x92, 0xda, 0x2f, 0x4b, 0x09, 0x84,
    0x3b, 0x9c, 0x43, 0xf4, 0x2a, 0x7f, 0x68, 0x81,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char ares_interfaces__srv__DetectObjects__TYPE_NAME[] = "ares_interfaces/srv/DetectObjects";
static char ares_interfaces__msg__SensedObject__TYPE_NAME[] = "ares_interfaces/msg/SensedObject";
static char ares_interfaces__srv__DetectObjects_Event__TYPE_NAME[] = "ares_interfaces/srv/DetectObjects_Event";
static char ares_interfaces__srv__DetectObjects_Request__TYPE_NAME[] = "ares_interfaces/srv/DetectObjects_Request";
static char ares_interfaces__srv__DetectObjects_Response__TYPE_NAME[] = "ares_interfaces/srv/DetectObjects_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char ares_interfaces__srv__DetectObjects__FIELD_NAME__request_message[] = "request_message";
static char ares_interfaces__srv__DetectObjects__FIELD_NAME__response_message[] = "response_message";
static char ares_interfaces__srv__DetectObjects__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field ares_interfaces__srv__DetectObjects__FIELDS[] = {
  {
    {ares_interfaces__srv__DetectObjects__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {ares_interfaces__srv__DetectObjects_Request__TYPE_NAME, 41, 41},
    },
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {ares_interfaces__srv__DetectObjects_Response__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {ares_interfaces__srv__DetectObjects_Event__TYPE_NAME, 39, 39},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription ares_interfaces__srv__DetectObjects__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {ares_interfaces__msg__SensedObject__TYPE_NAME, 32, 32},
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Event__TYPE_NAME, 39, 39},
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Request__TYPE_NAME, 41, 41},
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Response__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ares_interfaces__srv__DetectObjects__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ares_interfaces__srv__DetectObjects__TYPE_NAME, 33, 33},
      {ares_interfaces__srv__DetectObjects__FIELDS, 3, 3},
    },
    {ares_interfaces__srv__DetectObjects__REFERENCED_TYPE_DESCRIPTIONS, 7, 7},
  };
  if (!constructed) {
    assert(0 == memcmp(&ares_interfaces__msg__SensedObject__EXPECTED_HASH, ares_interfaces__msg__SensedObject__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = ares_interfaces__msg__SensedObject__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = ares_interfaces__srv__DetectObjects_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = ares_interfaces__srv__DetectObjects_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = ares_interfaces__srv__DetectObjects_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char ares_interfaces__srv__DetectObjects_Request__FIELD_NAME__trigger[] = "trigger";

static rosidl_runtime_c__type_description__Field ares_interfaces__srv__DetectObjects_Request__FIELDS[] = {
  {
    {ares_interfaces__srv__DetectObjects_Request__FIELD_NAME__trigger, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ares_interfaces__srv__DetectObjects_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ares_interfaces__srv__DetectObjects_Request__TYPE_NAME, 41, 41},
      {ares_interfaces__srv__DetectObjects_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char ares_interfaces__srv__DetectObjects_Response__FIELD_NAME__sensed_objects[] = "sensed_objects";

static rosidl_runtime_c__type_description__Field ares_interfaces__srv__DetectObjects_Response__FIELDS[] = {
  {
    {ares_interfaces__srv__DetectObjects_Response__FIELD_NAME__sensed_objects, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {ares_interfaces__msg__SensedObject__TYPE_NAME, 32, 32},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription ares_interfaces__srv__DetectObjects_Response__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {ares_interfaces__msg__SensedObject__TYPE_NAME, 32, 32},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ares_interfaces__srv__DetectObjects_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ares_interfaces__srv__DetectObjects_Response__TYPE_NAME, 42, 42},
      {ares_interfaces__srv__DetectObjects_Response__FIELDS, 1, 1},
    },
    {ares_interfaces__srv__DetectObjects_Response__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&ares_interfaces__msg__SensedObject__EXPECTED_HASH, ares_interfaces__msg__SensedObject__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = ares_interfaces__msg__SensedObject__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char ares_interfaces__srv__DetectObjects_Event__FIELD_NAME__info[] = "info";
static char ares_interfaces__srv__DetectObjects_Event__FIELD_NAME__request[] = "request";
static char ares_interfaces__srv__DetectObjects_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field ares_interfaces__srv__DetectObjects_Event__FIELDS[] = {
  {
    {ares_interfaces__srv__DetectObjects_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {ares_interfaces__srv__DetectObjects_Request__TYPE_NAME, 41, 41},
    },
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {ares_interfaces__srv__DetectObjects_Response__TYPE_NAME, 42, 42},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription ares_interfaces__srv__DetectObjects_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {ares_interfaces__msg__SensedObject__TYPE_NAME, 32, 32},
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Request__TYPE_NAME, 41, 41},
    {NULL, 0, 0},
  },
  {
    {ares_interfaces__srv__DetectObjects_Response__TYPE_NAME, 42, 42},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ares_interfaces__srv__DetectObjects_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ares_interfaces__srv__DetectObjects_Event__TYPE_NAME, 39, 39},
      {ares_interfaces__srv__DetectObjects_Event__FIELDS, 3, 3},
    },
    {ares_interfaces__srv__DetectObjects_Event__REFERENCED_TYPE_DESCRIPTIONS, 6, 6},
  };
  if (!constructed) {
    assert(0 == memcmp(&ares_interfaces__msg__SensedObject__EXPECTED_HASH, ares_interfaces__msg__SensedObject__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = ares_interfaces__msg__SensedObject__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = ares_interfaces__srv__DetectObjects_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = ares_interfaces__srv__DetectObjects_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# DetectObjects.srv\n"
  "# Service to trigger object detection and return detected objects\n"
  "\n"
  "bool trigger\n"
  "---\n"
  "ares_interfaces/SensedObject[] sensed_objects\n"
  "";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
ares_interfaces__srv__DetectObjects__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ares_interfaces__srv__DetectObjects__TYPE_NAME, 33, 33},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 151, 151},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
ares_interfaces__srv__DetectObjects_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ares_interfaces__srv__DetectObjects_Request__TYPE_NAME, 41, 41},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
ares_interfaces__srv__DetectObjects_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ares_interfaces__srv__DetectObjects_Response__TYPE_NAME, 42, 42},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
ares_interfaces__srv__DetectObjects_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ares_interfaces__srv__DetectObjects_Event__TYPE_NAME, 39, 39},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ares_interfaces__srv__DetectObjects__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[8];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 8, 8};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ares_interfaces__srv__DetectObjects__get_individual_type_description_source(NULL),
    sources[1] = *ares_interfaces__msg__SensedObject__get_individual_type_description_source(NULL);
    sources[2] = *ares_interfaces__srv__DetectObjects_Event__get_individual_type_description_source(NULL);
    sources[3] = *ares_interfaces__srv__DetectObjects_Request__get_individual_type_description_source(NULL);
    sources[4] = *ares_interfaces__srv__DetectObjects_Response__get_individual_type_description_source(NULL);
    sources[5] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[6] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[7] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ares_interfaces__srv__DetectObjects_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ares_interfaces__srv__DetectObjects_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ares_interfaces__srv__DetectObjects_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ares_interfaces__srv__DetectObjects_Response__get_individual_type_description_source(NULL),
    sources[1] = *ares_interfaces__msg__SensedObject__get_individual_type_description_source(NULL);
    sources[2] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ares_interfaces__srv__DetectObjects_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[7];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 7, 7};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ares_interfaces__srv__DetectObjects_Event__get_individual_type_description_source(NULL),
    sources[1] = *ares_interfaces__msg__SensedObject__get_individual_type_description_source(NULL);
    sources[2] = *ares_interfaces__srv__DetectObjects_Request__get_individual_type_description_source(NULL);
    sources[3] = *ares_interfaces__srv__DetectObjects_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[6] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
