// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from servo:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef SERVO__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
#define SERVO__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "servo/msg/detail/control_message__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace servo
{

namespace msg
{

namespace builder
{

class Init_ControlMessage_input_pos_deg
{
public:
  explicit Init_ControlMessage_input_pos_deg(::servo::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  ::servo::msg::ControlMessage input_pos_deg(::servo::msg::ControlMessage::_input_pos_deg_type arg)
  {
    msg_.input_pos_deg = std::move(arg);
    return std::move(msg_);
  }

private:
  ::servo::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_vel_deg
{
public:
  explicit Init_ControlMessage_input_vel_deg(::servo::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_pos_deg input_vel_deg(::servo::msg::ControlMessage::_input_vel_deg_type arg)
  {
    msg_.input_vel_deg = std::move(arg);
    return Init_ControlMessage_input_pos_deg(msg_);
  }

private:
  ::servo::msg::ControlMessage msg_;
};

class Init_ControlMessage_control_mode
{
public:
  Init_ControlMessage_control_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlMessage_input_vel_deg control_mode(::servo::msg::ControlMessage::_control_mode_type arg)
  {
    msg_.control_mode = std::move(arg);
    return Init_ControlMessage_input_vel_deg(msg_);
  }

private:
  ::servo::msg::ControlMessage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::servo::msg::ControlMessage>()
{
  return servo::msg::builder::Init_ControlMessage_control_mode();
}

}  // namespace servo

#endif  // SERVO__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
