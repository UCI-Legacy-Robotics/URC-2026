// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from stepper_can:msg/ODriveStatus.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__MSG__DETAIL__O_DRIVE_STATUS__BUILDER_HPP_
#define STEPPER_CAN__MSG__DETAIL__O_DRIVE_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "stepper_can/msg/detail/o_drive_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace stepper_can
{

namespace msg
{

namespace builder
{

class Init_ODriveStatus_disarm_reason
{
public:
  explicit Init_ODriveStatus_disarm_reason(::stepper_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  ::stepper_can::msg::ODriveStatus disarm_reason(::stepper_can::msg::ODriveStatus::_disarm_reason_type arg)
  {
    msg_.disarm_reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::stepper_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_active_errors
{
public:
  explicit Init_ODriveStatus_active_errors(::stepper_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_disarm_reason active_errors(::stepper_can::msg::ODriveStatus::_active_errors_type arg)
  {
    msg_.active_errors = std::move(arg);
    return Init_ODriveStatus_disarm_reason(msg_);
  }

private:
  ::stepper_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_motor_temperature
{
public:
  explicit Init_ODriveStatus_motor_temperature(::stepper_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_active_errors motor_temperature(::stepper_can::msg::ODriveStatus::_motor_temperature_type arg)
  {
    msg_.motor_temperature = std::move(arg);
    return Init_ODriveStatus_active_errors(msg_);
  }

private:
  ::stepper_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_fet_temperature
{
public:
  explicit Init_ODriveStatus_fet_temperature(::stepper_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_motor_temperature fet_temperature(::stepper_can::msg::ODriveStatus::_fet_temperature_type arg)
  {
    msg_.fet_temperature = std::move(arg);
    return Init_ODriveStatus_motor_temperature(msg_);
  }

private:
  ::stepper_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_bus_current
{
public:
  explicit Init_ODriveStatus_bus_current(::stepper_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_fet_temperature bus_current(::stepper_can::msg::ODriveStatus::_bus_current_type arg)
  {
    msg_.bus_current = std::move(arg);
    return Init_ODriveStatus_fet_temperature(msg_);
  }

private:
  ::stepper_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_bus_voltage
{
public:
  Init_ODriveStatus_bus_voltage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ODriveStatus_bus_current bus_voltage(::stepper_can::msg::ODriveStatus::_bus_voltage_type arg)
  {
    msg_.bus_voltage = std::move(arg);
    return Init_ODriveStatus_bus_current(msg_);
  }

private:
  ::stepper_can::msg::ODriveStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::stepper_can::msg::ODriveStatus>()
{
  return stepper_can::msg::builder::Init_ODriveStatus_bus_voltage();
}

}  // namespace stepper_can

#endif  // STEPPER_CAN__MSG__DETAIL__O_DRIVE_STATUS__BUILDER_HPP_
