// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice

#ifndef DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__STRUCT_HPP_
#define DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__drive_teleop__msg__DriveControlMessage __attribute__((deprecated))
#else
# define DEPRECATED__drive_teleop__msg__DriveControlMessage __declspec(deprecated)
#endif

namespace drive_teleop
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DriveControlMessage_
{
  using Type = DriveControlMessage_<ContainerAllocator>;

  explicit DriveControlMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_input_pwm = 0l;
      this->right_input_pwm = 0l;
    }
  }

  explicit DriveControlMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->left_input_pwm = 0l;
      this->right_input_pwm = 0l;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _left_input_pwm_type =
    int32_t;
  _left_input_pwm_type left_input_pwm;
  using _right_input_pwm_type =
    int32_t;
  _right_input_pwm_type right_input_pwm;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__left_input_pwm(
    const int32_t & _arg)
  {
    this->left_input_pwm = _arg;
    return *this;
  }
  Type & set__right_input_pwm(
    const int32_t & _arg)
  {
    this->right_input_pwm = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    drive_teleop::msg::DriveControlMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const drive_teleop::msg::DriveControlMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      drive_teleop::msg::DriveControlMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      drive_teleop::msg::DriveControlMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__drive_teleop__msg__DriveControlMessage
    std::shared_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__drive_teleop__msg__DriveControlMessage
    std::shared_ptr<drive_teleop::msg::DriveControlMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DriveControlMessage_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->left_input_pwm != other.left_input_pwm) {
      return false;
    }
    if (this->right_input_pwm != other.right_input_pwm) {
      return false;
    }
    return true;
  }
  bool operator!=(const DriveControlMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DriveControlMessage_

// alias to use template instance with default allocator
using DriveControlMessage =
  drive_teleop::msg::DriveControlMessage_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace drive_teleop

#endif  // DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__STRUCT_HPP_
