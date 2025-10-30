// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/msg/sensed_object.hpp"


#ifndef ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__TRAITS_HPP_
#define ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "ares_interfaces/msg/detail/sensed_object__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'map_coords'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace ares_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const SensedObject & msg,
  std::ostream & out)
{
  out << "{";
  // member: class_name
  {
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << ", ";
  }

  // member: map_coords
  {
    out << "map_coords: ";
    to_flow_style_yaml(msg.map_coords, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SensedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: class_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << "\n";
  }

  // member: map_coords
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "map_coords:\n";
    to_block_style_yaml(msg.map_coords, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SensedObject & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace ares_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use ares_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ares_interfaces::msg::SensedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  ares_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ares_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const ares_interfaces::msg::SensedObject & msg)
{
  return ares_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<ares_interfaces::msg::SensedObject>()
{
  return "ares_interfaces::msg::SensedObject";
}

template<>
inline const char * name<ares_interfaces::msg::SensedObject>()
{
  return "ares_interfaces/msg/SensedObject";
}

template<>
struct has_fixed_size<ares_interfaces::msg::SensedObject>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<ares_interfaces::msg::SensedObject>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<ares_interfaces::msg::SensedObject>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__TRAITS_HPP_
