// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from cubemars_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__cubemars_can__msg__ControlMessage __attribute__((deprecated))
#else
# define DEPRECATED__cubemars_can__msg__ControlMessage __declspec(deprecated)
#endif

namespace cubemars_can
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
      this->input_vel_rpm = 0.0f;
      this->input_pos_deg = 0.0f;
      this->set_vel_limit_rpm = 0.0f;
      this->set_accel_limit_rpm_s = 0.0f;
      this->set_origin = 0;
    }
  }

  explicit ControlMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->control_mode = 0ul;
      this->input_vel_rpm = 0.0f;
      this->input_pos_deg = 0.0f;
      this->set_vel_limit_rpm = 0.0f;
      this->set_accel_limit_rpm_s = 0.0f;
      this->set_origin = 0;
    }
  }

  // field types and members
  using _control_mode_type =
    uint32_t;
  _control_mode_type control_mode;
  using _input_vel_rpm_type =
    float;
  _input_vel_rpm_type input_vel_rpm;
  using _input_pos_deg_type =
    float;
  _input_pos_deg_type input_pos_deg;
  using _set_vel_limit_rpm_type =
    float;
  _set_vel_limit_rpm_type set_vel_limit_rpm;
  using _set_accel_limit_rpm_s_type =
    float;
  _set_accel_limit_rpm_s_type set_accel_limit_rpm_s;
  using _set_origin_type =
    uint8_t;
  _set_origin_type set_origin;

  // setters for named parameter idiom
  Type & set__control_mode(
    const uint32_t & _arg)
  {
    this->control_mode = _arg;
    return *this;
  }
  Type & set__input_vel_rpm(
    const float & _arg)
  {
    this->input_vel_rpm = _arg;
    return *this;
  }
  Type & set__input_pos_deg(
    const float & _arg)
  {
    this->input_pos_deg = _arg;
    return *this;
  }
  Type & set__set_vel_limit_rpm(
    const float & _arg)
  {
    this->set_vel_limit_rpm = _arg;
    return *this;
  }
  Type & set__set_accel_limit_rpm_s(
    const float & _arg)
  {
    this->set_accel_limit_rpm_s = _arg;
    return *this;
  }
  Type & set__set_origin(
    const uint8_t & _arg)
  {
    this->set_origin = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cubemars_can::msg::ControlMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const cubemars_can::msg::ControlMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cubemars_can::msg::ControlMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cubemars_can::msg::ControlMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cubemars_can__msg__ControlMessage
    std::shared_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cubemars_can__msg__ControlMessage
    std::shared_ptr<cubemars_can::msg::ControlMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlMessage_ & other) const
  {
    if (this->control_mode != other.control_mode) {
      return false;
    }
    if (this->input_vel_rpm != other.input_vel_rpm) {
      return false;
    }
    if (this->input_pos_deg != other.input_pos_deg) {
      return false;
    }
    if (this->set_vel_limit_rpm != other.set_vel_limit_rpm) {
      return false;
    }
    if (this->set_accel_limit_rpm_s != other.set_accel_limit_rpm_s) {
      return false;
    }
    if (this->set_origin != other.set_origin) {
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
  cubemars_can::msg::ControlMessage_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace cubemars_can

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__STRUCT_HPP_
