// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ares_interfaces:srv/DetectObjects.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ares_interfaces/srv/detect_objects.hpp"


#ifndef ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__STRUCT_HPP_
#define ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__ares_interfaces__srv__DetectObjects_Request __attribute__((deprecated))
#else
# define DEPRECATED__ares_interfaces__srv__DetectObjects_Request __declspec(deprecated)
#endif

namespace ares_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DetectObjects_Request_
{
  using Type = DetectObjects_Request_<ContainerAllocator>;

  explicit DetectObjects_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->trigger = false;
    }
  }

  explicit DetectObjects_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->trigger = false;
    }
  }

  // field types and members
  using _trigger_type =
    bool;
  _trigger_type trigger;

  // setters for named parameter idiom
  Type & set__trigger(
    const bool & _arg)
  {
    this->trigger = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ares_interfaces__srv__DetectObjects_Request
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ares_interfaces__srv__DetectObjects_Request
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectObjects_Request_ & other) const
  {
    if (this->trigger != other.trigger) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectObjects_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectObjects_Request_

// alias to use template instance with default allocator
using DetectObjects_Request =
  ares_interfaces::srv::DetectObjects_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ares_interfaces


// Include directives for member types
// Member 'sensed_objects'
#include "ares_interfaces/msg/detail/sensed_object__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__ares_interfaces__srv__DetectObjects_Response __attribute__((deprecated))
#else
# define DEPRECATED__ares_interfaces__srv__DetectObjects_Response __declspec(deprecated)
#endif

namespace ares_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DetectObjects_Response_
{
  using Type = DetectObjects_Response_<ContainerAllocator>;

  explicit DetectObjects_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit DetectObjects_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _sensed_objects_type =
    std::vector<ares_interfaces::msg::SensedObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<ares_interfaces::msg::SensedObject_<ContainerAllocator>>>;
  _sensed_objects_type sensed_objects;

  // setters for named parameter idiom
  Type & set__sensed_objects(
    const std::vector<ares_interfaces::msg::SensedObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<ares_interfaces::msg::SensedObject_<ContainerAllocator>>> & _arg)
  {
    this->sensed_objects = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ares_interfaces__srv__DetectObjects_Response
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ares_interfaces__srv__DetectObjects_Response
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectObjects_Response_ & other) const
  {
    if (this->sensed_objects != other.sensed_objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectObjects_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectObjects_Response_

// alias to use template instance with default allocator
using DetectObjects_Response =
  ares_interfaces::srv::DetectObjects_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ares_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__ares_interfaces__srv__DetectObjects_Event __attribute__((deprecated))
#else
# define DEPRECATED__ares_interfaces__srv__DetectObjects_Event __declspec(deprecated)
#endif

namespace ares_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DetectObjects_Event_
{
  using Type = DetectObjects_Event_<ContainerAllocator>;

  explicit DetectObjects_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit DetectObjects_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<ares_interfaces::srv::DetectObjects_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<ares_interfaces::srv::DetectObjects_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ares_interfaces__srv__DetectObjects_Event
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ares_interfaces__srv__DetectObjects_Event
    std::shared_ptr<ares_interfaces::srv::DetectObjects_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectObjects_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectObjects_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectObjects_Event_

// alias to use template instance with default allocator
using DetectObjects_Event =
  ares_interfaces::srv::DetectObjects_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace ares_interfaces

namespace ares_interfaces
{

namespace srv
{

struct DetectObjects
{
  using Request = ares_interfaces::srv::DetectObjects_Request;
  using Response = ares_interfaces::srv::DetectObjects_Response;
  using Event = ares_interfaces::srv::DetectObjects_Event;
};

}  // namespace srv

}  // namespace ares_interfaces

#endif  // ARES_INTERFACES__SRV__DETAIL__DETECT_OBJECTS__STRUCT_HPP_
