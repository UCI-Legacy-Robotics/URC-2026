// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from cubemars_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "cubemars_can/msg/detail/control_message__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace cubemars_can
{

namespace msg
{

namespace builder
{

class Init_ControlMessage_set_origin
{
public:
  explicit Init_ControlMessage_set_origin(::cubemars_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  ::cubemars_can::msg::ControlMessage set_origin(::cubemars_can::msg::ControlMessage::_set_origin_type arg)
  {
    msg_.set_origin = std::move(arg);
    return std::move(msg_);
  }

private:
  ::cubemars_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_set_accel_limit_rpm_s
{
public:
  explicit Init_ControlMessage_set_accel_limit_rpm_s(::cubemars_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_set_origin set_accel_limit_rpm_s(::cubemars_can::msg::ControlMessage::_set_accel_limit_rpm_s_type arg)
  {
    msg_.set_accel_limit_rpm_s = std::move(arg);
    return Init_ControlMessage_set_origin(msg_);
  }

private:
  ::cubemars_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_set_vel_limit_rpm
{
public:
  explicit Init_ControlMessage_set_vel_limit_rpm(::cubemars_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_set_accel_limit_rpm_s set_vel_limit_rpm(::cubemars_can::msg::ControlMessage::_set_vel_limit_rpm_type arg)
  {
    msg_.set_vel_limit_rpm = std::move(arg);
    return Init_ControlMessage_set_accel_limit_rpm_s(msg_);
  }

private:
  ::cubemars_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_pos_deg
{
public:
  explicit Init_ControlMessage_input_pos_deg(::cubemars_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_set_vel_limit_rpm input_pos_deg(::cubemars_can::msg::ControlMessage::_input_pos_deg_type arg)
  {
    msg_.input_pos_deg = std::move(arg);
    return Init_ControlMessage_set_vel_limit_rpm(msg_);
  }

private:
  ::cubemars_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_vel_rpm
{
public:
  explicit Init_ControlMessage_input_vel_rpm(::cubemars_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_pos_deg input_vel_rpm(::cubemars_can::msg::ControlMessage::_input_vel_rpm_type arg)
  {
    msg_.input_vel_rpm = std::move(arg);
    return Init_ControlMessage_input_pos_deg(msg_);
  }

private:
  ::cubemars_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_control_mode
{
public:
  Init_ControlMessage_control_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlMessage_input_vel_rpm control_mode(::cubemars_can::msg::ControlMessage::_control_mode_type arg)
  {
    msg_.control_mode = std::move(arg);
    return Init_ControlMessage_input_vel_rpm(msg_);
  }

private:
  ::cubemars_can::msg::ControlMessage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::cubemars_can::msg::ControlMessage>()
{
  return cubemars_can::msg::builder::Init_ControlMessage_control_mode();
}

}  // namespace cubemars_can

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
