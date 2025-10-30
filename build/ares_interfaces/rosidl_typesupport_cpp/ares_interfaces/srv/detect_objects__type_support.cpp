// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "ares_interfaces/srv/detail/detect_objects__functions.h"
#include "ares_interfaces/srv/detail/detect_objects__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace ares_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DetectObjects_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DetectObjects_Request_type_support_ids_t;

static const _DetectObjects_Request_type_support_ids_t _DetectObjects_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DetectObjects_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DetectObjects_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DetectObjects_Request_type_support_symbol_names_t _DetectObjects_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ares_interfaces, srv, DetectObjects_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, ares_interfaces, srv, DetectObjects_Request)),
  }
};

typedef struct _DetectObjects_Request_type_support_data_t
{
  void * data[2];
} _DetectObjects_Request_type_support_data_t;

static _DetectObjects_Request_type_support_data_t _DetectObjects_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DetectObjects_Request_message_typesupport_map = {
  2,
  "ares_interfaces",
  &_DetectObjects_Request_message_typesupport_ids.typesupport_identifier[0],
  &_DetectObjects_Request_message_typesupport_symbol_names.symbol_name[0],
  &_DetectObjects_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DetectObjects_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DetectObjects_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Request__get_type_hash,
  &ares_interfaces__srv__DetectObjects_Request__get_type_description,
  &ares_interfaces__srv__DetectObjects_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace ares_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Request>()
{
  return &::ares_interfaces::srv::rosidl_typesupport_cpp::DetectObjects_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, ares_interfaces, srv, DetectObjects_Request)() {
  return get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__functions.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace ares_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DetectObjects_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DetectObjects_Response_type_support_ids_t;

static const _DetectObjects_Response_type_support_ids_t _DetectObjects_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DetectObjects_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DetectObjects_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DetectObjects_Response_type_support_symbol_names_t _DetectObjects_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ares_interfaces, srv, DetectObjects_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, ares_interfaces, srv, DetectObjects_Response)),
  }
};

typedef struct _DetectObjects_Response_type_support_data_t
{
  void * data[2];
} _DetectObjects_Response_type_support_data_t;

static _DetectObjects_Response_type_support_data_t _DetectObjects_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DetectObjects_Response_message_typesupport_map = {
  2,
  "ares_interfaces",
  &_DetectObjects_Response_message_typesupport_ids.typesupport_identifier[0],
  &_DetectObjects_Response_message_typesupport_symbol_names.symbol_name[0],
  &_DetectObjects_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DetectObjects_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DetectObjects_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Response__get_type_hash,
  &ares_interfaces__srv__DetectObjects_Response__get_type_description,
  &ares_interfaces__srv__DetectObjects_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace ares_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Response>()
{
  return &::ares_interfaces::srv::rosidl_typesupport_cpp::DetectObjects_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, ares_interfaces, srv, DetectObjects_Response)() {
  return get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__functions.h"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace ares_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DetectObjects_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DetectObjects_Event_type_support_ids_t;

static const _DetectObjects_Event_type_support_ids_t _DetectObjects_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DetectObjects_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DetectObjects_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DetectObjects_Event_type_support_symbol_names_t _DetectObjects_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ares_interfaces, srv, DetectObjects_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, ares_interfaces, srv, DetectObjects_Event)),
  }
};

typedef struct _DetectObjects_Event_type_support_data_t
{
  void * data[2];
} _DetectObjects_Event_type_support_data_t;

static _DetectObjects_Event_type_support_data_t _DetectObjects_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DetectObjects_Event_message_typesupport_map = {
  2,
  "ares_interfaces",
  &_DetectObjects_Event_message_typesupport_ids.typesupport_identifier[0],
  &_DetectObjects_Event_message_typesupport_symbol_names.symbol_name[0],
  &_DetectObjects_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t DetectObjects_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DetectObjects_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &ares_interfaces__srv__DetectObjects_Event__get_type_hash,
  &ares_interfaces__srv__DetectObjects_Event__get_type_description,
  &ares_interfaces__srv__DetectObjects_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace ares_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Event>()
{
  return &::ares_interfaces::srv::rosidl_typesupport_cpp::DetectObjects_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, ares_interfaces, srv, DetectObjects_Event)() {
  return get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "ares_interfaces/srv/detail/detect_objects__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace ares_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _DetectObjects_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _DetectObjects_type_support_ids_t;

static const _DetectObjects_type_support_ids_t _DetectObjects_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _DetectObjects_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _DetectObjects_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _DetectObjects_type_support_symbol_names_t _DetectObjects_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ares_interfaces, srv, DetectObjects)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, ares_interfaces, srv, DetectObjects)),
  }
};

typedef struct _DetectObjects_type_support_data_t
{
  void * data[2];
} _DetectObjects_type_support_data_t;

static _DetectObjects_type_support_data_t _DetectObjects_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _DetectObjects_service_typesupport_map = {
  2,
  "ares_interfaces",
  &_DetectObjects_service_typesupport_ids.typesupport_identifier[0],
  &_DetectObjects_service_typesupport_symbol_names.symbol_name[0],
  &_DetectObjects_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t DetectObjects_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_DetectObjects_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<ares_interfaces::srv::DetectObjects_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<ares_interfaces::srv::DetectObjects>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<ares_interfaces::srv::DetectObjects>,
  &ares_interfaces__srv__DetectObjects__get_type_hash,
  &ares_interfaces__srv__DetectObjects__get_type_description,
  &ares_interfaces__srv__DetectObjects__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace ares_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<ares_interfaces::srv::DetectObjects>()
{
  return &::ares_interfaces::srv::rosidl_typesupport_cpp::DetectObjects_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, ares_interfaces, srv, DetectObjects)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<ares_interfaces::srv::DetectObjects>();
}

#ifdef __cplusplus
}
#endif
