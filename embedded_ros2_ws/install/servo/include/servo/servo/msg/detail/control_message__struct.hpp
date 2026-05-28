// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from servo:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef SERVO__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_HPP_
#define SERVO__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__servo__msg__ControlMessage __attribute__((deprecated))
#else
# define DEPRECATED__servo__msg__ControlMessage __declspec(deprecated)
#endif

namespace servo
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ControlMessage_
{
  using Type = ControlMessage_<ContainerAllocator>;

  explicit ControlMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->control_mode = 0ul;
      this->input_vel_deg = 0.0f;
      this->input_pos_deg = 0.0f;
    }
  }

  explicit ControlMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->control_mode = 0ul;
      this->input_vel_deg = 0.0f;
      this->input_pos_deg = 0.0f;
    }
  }

  // field types and members
  using _control_mode_type =
    uint32_t;
  _control_mode_type control_mode;
  using _input_vel_deg_type =
    float;
  _input_vel_deg_type input_vel_deg;
  using _input_pos_deg_type =
    float;
  _input_pos_deg_type input_pos_deg;

  // setters for named parameter idiom
  Type & set__control_mode(
    const uint32_t & _arg)
  {
    this->control_mode = _arg;
    return *this;
  }
  Type & set__input_vel_deg(
    const float & _arg)
  {
    this->input_vel_deg = _arg;
    return *this;
  }
  Type & set__input_pos_deg(
    const float & _arg)
  {
    this->input_pos_deg = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    servo::msg::ControlMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const servo::msg::ControlMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<servo::msg::ControlMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<servo::msg::ControlMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      servo::msg::ControlMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<servo::msg::ControlMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      servo::msg::ControlMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<servo::msg::ControlMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<servo::msg::ControlMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<servo::msg::ControlMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__servo__msg__ControlMessage
    std::shared_ptr<servo::msg::ControlMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__servo__msg__ControlMessage
    std::shared_ptr<servo::msg::ControlMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlMessage_ & other) const
  {
    if (this->control_mode != other.control_mode) {
      return false;
    }
    if (this->input_vel_deg != other.input_vel_deg) {
      return false;
    }
    if (this->input_pos_deg != other.input_pos_deg) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControlMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControlMessage_

// alias to use template instance with default allocator
using ControlMessage =
  servo::msg::ControlMessage_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace servo

#endif  // SERVO__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_HPP_
