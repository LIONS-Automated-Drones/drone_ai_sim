// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ares_interfaces:msg/SensedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/msg/sensed_object.hpp"


#ifndef ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__STRUCT_HPP_
#define ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'map_coords'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__ares_interfaces__msg__SensedObject __attribute__((deprecated))
#else
# define DEPRECATED__ares_interfaces__msg__SensedObject __declspec(deprecated)
#endif

namespace ares_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SensedObject_
{
  using Type = SensedObject_<ContainerAllocator>;

  explicit SensedObject_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : map_coords(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->class_name = "";
    }
  }

  explicit SensedObject_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : class_name(_alloc),
    map_coords(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->class_name = "";
    }
  }

  // field types and members
  using _class_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _class_name_type class_name;
  using _map_coords_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _map_coords_type map_coords;

  // setters for named parameter idiom
  Type & set__class_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->class_name = _arg;
    return *this;
  }
  Type & set__map_coords(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->map_coords = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ares_interfaces::msg::SensedObject_<ContainerAllocator> *;
  using ConstRawPtr =
    const ares_interfaces::msg::SensedObject_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::msg::SensedObject_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::msg::SensedObject_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ares_interfaces__msg__SensedObject
    std::shared_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ares_interfaces__msg__SensedObject
    std::shared_ptr<ares_interfaces::msg::SensedObject_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SensedObject_ & other) const
  {
    if (this->class_name != other.class_name) {
      return false;
    }
    if (this->map_coords != other.map_coords) {
      return false;
    }
    return true;
  }
  bool operator!=(const SensedObject_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SensedObject_

// alias to use template instance with default allocator
using SensedObject =
  ares_interfaces::msg::SensedObject_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace ares_interfaces

#endif  // ARES_INTERFACES__MSG__DETAIL__SENSED_OBJECT__STRUCT_HPP_
