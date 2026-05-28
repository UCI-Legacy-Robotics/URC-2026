// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__BUILDER_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cubemars_can/msg/detail/controller_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cubemars_can
{

namespace msg
{

namespace builder
{

class Init_ControllerStatus_active_errors
{
public:
  explicit Init_ControllerStatus_active_errors(::cubemars_can::msg::ControllerStatus & msg)
  : msg_(msg)
  {}
  ::cubemars_can::msg::ControllerStatus active_errors(::cubemars_can::msg::ControllerStatus::_active_errors_type arg)
  {
    msg_.active_errors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cubemars_can::msg::ControllerStatus msg_;
};

class Init_ControllerStatus_motor_temperature_c
{
public:
  explicit Init_ControllerStatus_motor_temperature_c(::cubemars_can::msg::ControllerStatus & msg)
  : msg_(msg)
  {}
  Init_ControllerStatus_active_errors motor_temperature_c(::cubemars_can::msg::ControllerStatus::_motor_temperature_c_type arg)
  {
    msg_.motor_temperature_c = std::move(arg);
    return Init_ControllerStatus_active_errors(msg_);
  }

private:
  ::cubemars_can::msg::ControllerStatus msg_;
};

class Init_ControllerStatus_motor_current_amps
{
public:
  explicit Init_ControllerStatus_motor_current_amps(::cubemars_can::msg::ControllerStatus & msg)
  : msg_(msg)
  {}
  Init_ControllerStatus_motor_temperature_c motor_current_amps(::cubemars_can::msg::ControllerStatus::_motor_current_amps_type arg)
  {
    msg_.motor_current_amps = std::move(arg);
    return Init_ControllerStatus_motor_temperature_c(msg_);
  }

private:
  ::cubemars_can::msg::ControllerStatus msg_;
};

class Init_ControllerStatus_vel_estimate_rpm
{
public:
  explicit Init_ControllerStatus_vel_estimate_rpm(::cubemars_can::msg::ControllerStatus & msg)
  : msg_(msg)
  {}
  Init_ControllerStatus_motor_current_amps vel_estimate_rpm(::cubemars_can::msg::ControllerStatus::_vel_estimate_rpm_type arg)
  {
    msg_.vel_estimate_rpm = std::move(arg);
    return Init_ControllerStatus_motor_current_amps(msg_);
  }

private:
  ::cubemars_can::msg::ControllerStatus msg_;
};

class Init_ControllerStatus_pos_estimate_deg
{
public:
  Init_ControllerStatus_pos_estimate_deg()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControllerStatus_vel_estimate_rpm pos_estimate_deg(::cubemars_can::msg::ControllerStatus::_pos_estimate_deg_type arg)
  {
    msg_.pos_estimate_deg = std::move(arg);
    return Init_ControllerStatus_vel_estimate_rpm(msg_);
  }

private:
  ::cubemars_can::msg::ControllerStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cubemars_can::msg::ControllerStatus>()
{
  return cubemars_can::msg::builder::Init_ControllerStatus_pos_estimate_deg();
}

}  // namespace cubemars_can

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__BUILDER_HPP_
