// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/srv/detect_objects.hpp"


#ifndef ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__BUILDER_HPP_
#define ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ares_interfaces/srv/detail/detect_objects__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ares_interfaces
{

namespace srv
{

namespace builder
{

class Init_DetectObjects_Request_trigger
{
public:
  Init_DetectObjects_Request_trigger()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::ares_interfaces::srv::DetectObjects_Request trigger(::ares_interfaces::srv::DetectObjects_Request::_trigger_type arg)
  {
    msg_.trigger = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ares_interfaces::srv::DetectObjects_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ares_interfaces::srv::DetectObjects_Request>()
{
  return ares_interfaces::srv::builder::Init_DetectObjects_Request_trigger();
}

}  // namespace ares_interfaces


namespace ares_interfaces
{

namespace srv
{

namespace builder
{

class Init_DetectObjects_Response_sensed_objects
{
public:
  Init_DetectObjects_Response_sensed_objects()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::ares_interfaces::srv::DetectObjects_Response sensed_objects(::ares_interfaces::srv::DetectObjects_Response::_sensed_objects_type arg)
  {
    msg_.sensed_objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ares_interfaces::srv::DetectObjects_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ares_interfaces::srv::DetectObjects_Response>()
{
  return ares_interfaces::srv::builder::Init_DetectObjects_Response_sensed_objects();
}

}  // namespace ares_interfaces


namespace ares_interfaces
{

namespace srv
{

namespace builder
{

class Init_DetectObjects_Event_response
{
public:
  explicit Init_DetectObjects_Event_response(::ares_interfaces::srv::DetectObjects_Event & msg)
  : msg_(msg)
  {}
  ::ares_interfaces::srv::DetectObjects_Event response(::ares_interfaces::srv::DetectObjects_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ares_interfaces::srv::DetectObjects_Event msg_;
};

class Init_DetectObjects_Event_request
{
public:
  explicit Init_DetectObjects_Event_request(::ares_interfaces::srv::DetectObjects_Event & msg)
  : msg_(msg)
  {}
  Init_DetectObjects_Event_response request(::ares_interfaces::srv::DetectObjects_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_DetectObjects_Event_response(msg_);
  }

private:
  ::ares_interfaces::srv::DetectObjects_Event msg_;
};

class Init_DetectObjects_Event_info
{
public:
  Init_DetectObjects_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectObjects_Event_request info(::ares_interfaces::srv::DetectObjects_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_DetectObjects_Event_request(msg_);
  }

private:
  ::ares_interfaces::srv::DetectObjects_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::ares_interfaces::srv::DetectObjects_Event>()
{
  return ares_interfaces::srv::builder::Init_DetectObjects_Event_info();
}

}  // namespace ares_interfaces

#endif  // ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__BUILDER_HPP_
