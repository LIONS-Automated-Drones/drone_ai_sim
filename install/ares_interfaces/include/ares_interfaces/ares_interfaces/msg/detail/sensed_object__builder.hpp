// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/msg/sensed_object.hpp"


#ifndef ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__BUILDER_HPP_
#define ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ares_interfaces/msg/detail/sensed_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ares_interfaces
{

namespace msg
{

namespace builder
{

class Init_SensedObject_map_coords
{
public:
  explicit Init_SensedObject_map_coords(::ares_interfaces::msg::SensedObject & msg)
  : msg_(msg)
  {}
  ::ares_interfaces::msg::SensedObject map_coords(::ares_interfaces::msg::SensedObject::_map_coords_type arg)
  {
    msg_.map_coords = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ares_interfaces::msg::SensedObject msg_;
};

class Init_SensedObject_class_name
{
public:
  Init_SensedObject_class_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SensedObject_map_coords class_name(::ares_interfaces::msg::SensedObject::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_SensedObject_map_coords(msg_);
  }

private:
  ::ares_interfaces::msg::SensedObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::ares_interfaces::msg::SensedObject>()
{
  return ares_interfaces::msg::builder::Init_SensedObject_class_name();
}

}  // namespace ares_interfaces

#endif  // ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__BUILDER_HPP_
