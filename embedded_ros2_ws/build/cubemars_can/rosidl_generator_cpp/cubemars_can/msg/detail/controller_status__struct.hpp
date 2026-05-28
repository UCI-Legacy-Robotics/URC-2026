// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__STRUCT_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__cubemars_can__msg__ControllerStatus __attribute__((deprecated))
#else
# define DEPRECATED__cubemars_can__msg__ControllerStatus __declspec(deprecated)
#endif

namespace cubemars_can
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ControllerStatus_
{
  using Type = ControllerStatus_<ContainerAllocator>;

  explicit ControllerStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pos_estimate_deg = 0.0f;
      this->vel_estimate_rpm = 0.0f;
      this->motor_current_amps = 0.0f;
      this->motor_temperature_c = 0;
      this->active_errors = 0;
    }
  }

  explicit ControllerStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pos_estimate_deg = 0.0f;
      this->vel_estimate_rpm = 0.0f;
      this->motor_current_amps = 0.0f;
      this->motor_temperature_c = 0;
      this->active_errors = 0;
    }
  }

  // field types and members
  using _pos_estimate_deg_type =
    float;
  _pos_estimate_deg_type pos_estimate_deg;
  using _vel_estimate_rpm_type =
    float;
  _vel_estimate_rpm_type vel_estimate_rpm;
  using _motor_current_amps_type =
    float;
  _motor_current_amps_type motor_current_amps;
  using _motor_temperature_c_type =
    int8_t;
  _motor_temperature_c_type motor_temperature_c;
  using _active_errors_type =
    uint8_t;
  _active_errors_type active_errors;

  // setters for named parameter idiom
  Type & set__pos_estimate_deg(
    const float & _arg)
  {
    this->pos_estimate_deg = _arg;
    return *this;
  }
  Type & set__vel_estimate_rpm(
    const float & _arg)
  {
    this->vel_estimate_rpm = _arg;
    return *this;
  }
  Type & set__motor_current_amps(
    const float & _arg)
  {
    this->motor_current_amps = _arg;
    return *this;
  }
  Type & set__motor_temperature_c(
    const int8_t & _arg)
  {
    this->motor_temperature_c = _arg;
    return *this;
  }
  Type & set__active_errors(
    const uint8_t & _arg)
  {
    this->active_errors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    cubemars_can::msg::ControllerStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const cubemars_can::msg::ControllerStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      cubemars_can::msg::ControllerStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      cubemars_can::msg::ControllerStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__cubemars_can__msg__ControllerStatus
    std::shared_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__cubemars_can__msg__ControllerStatus
    std::shared_ptr<cubemars_can::msg::ControllerStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControllerStatus_ & other) const
  {
    if (this->pos_estimate_deg != other.pos_estimate_deg) {
      return false;
    }
    if (this->vel_estimate_rpm != other.vel_estimate_rpm) {
      return false;
    }
    if (this->motor_current_amps != other.motor_current_amps) {
      return false;
    }
    if (this->motor_temperature_c != other.motor_temperature_c) {
      return false;
    }
    if (this->active_errors != other.active_errors) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControllerStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControllerStatus_

// alias to use template instance with default allocator
using ControllerStatus =
  cubemars_can::msg::ControllerStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace cubemars_can

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__STRUCT_HPP_
