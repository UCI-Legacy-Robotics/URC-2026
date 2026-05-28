// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from yellowjacket_can:msg/ODriveStatus.idl
// generated code does not contain a copyright notice

#ifndef YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__BUILDER_HPP_
#define YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "yellowjacket_can/msg/detail/o_drive_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace yellowjacket_can
{

namespace msg
{

namespace builder
{

class Init_ODriveStatus_disarm_reason
{
public:
  explicit Init_ODriveStatus_disarm_reason(::yellowjacket_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  ::yellowjacket_can::msg::ODriveStatus disarm_reason(::yellowjacket_can::msg::ODriveStatus::_disarm_reason_type arg)
  {
    msg_.disarm_reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yellowjacket_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_active_errors
{
public:
  explicit Init_ODriveStatus_active_errors(::yellowjacket_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_disarm_reason active_errors(::yellowjacket_can::msg::ODriveStatus::_active_errors_type arg)
  {
    msg_.active_errors = std::move(arg);
    return Init_ODriveStatus_disarm_reason(msg_);
  }

private:
  ::yellowjacket_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_motor_temperature
{
public:
  explicit Init_ODriveStatus_motor_temperature(::yellowjacket_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_active_errors motor_temperature(::yellowjacket_can::msg::ODriveStatus::_motor_temperature_type arg)
  {
    msg_.motor_temperature = std::move(arg);
    return Init_ODriveStatus_active_errors(msg_);
  }

private:
  ::yellowjacket_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_fet_temperature
{
public:
  explicit Init_ODriveStatus_fet_temperature(::yellowjacket_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_motor_temperature fet_temperature(::yellowjacket_can::msg::ODriveStatus::_fet_temperature_type arg)
  {
    msg_.fet_temperature = std::move(arg);
    return Init_ODriveStatus_motor_temperature(msg_);
  }

private:
  ::yellowjacket_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_bus_current
{
public:
  explicit Init_ODriveStatus_bus_current(::yellowjacket_can::msg::ODriveStatus & msg)
  : msg_(msg)
  {}
  Init_ODriveStatus_fet_temperature bus_current(::yellowjacket_can::msg::ODriveStatus::_bus_current_type arg)
  {
    msg_.bus_current = std::move(arg);
    return Init_ODriveStatus_fet_temperature(msg_);
  }

private:
  ::yellowjacket_can::msg::ODriveStatus msg_;
};

class Init_ODriveStatus_bus_voltage
{
public:
  Init_ODriveStatus_bus_voltage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ODriveStatus_bus_current bus_voltage(::yellowjacket_can::msg::ODriveStatus::_bus_voltage_type arg)
  {
    msg_.bus_voltage = std::move(arg);
    return Init_ODriveStatus_bus_current(msg_);
  }

private:
  ::yellowjacket_can::msg::ODriveStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::yellowjacket_can::msg::ODriveStatus>()
{
  return yellowjacket_can::msg::builder::Init_ODriveStatus_bus_voltage();
}

}  // namespace yellowjacket_can

#endif  // YELLOWJACKET_CAN__MSG__DETAIL__O_DRIVE_STATUS__BUILDER_HPP_
