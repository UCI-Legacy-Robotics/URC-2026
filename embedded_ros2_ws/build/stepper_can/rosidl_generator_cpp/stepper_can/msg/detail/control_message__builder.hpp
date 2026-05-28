// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from stepper_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
#define STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "stepper_can/msg/detail/control_message__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace stepper_can
{

namespace msg
{

namespace builder
{

class Init_ControlMessage_input_torque
{
public:
  explicit Init_ControlMessage_input_torque(::stepper_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  ::stepper_can::msg::ControlMessage input_torque(::stepper_can::msg::ControlMessage::_input_torque_type arg)
  {
    msg_.input_torque = std::move(arg);
    return std::move(msg_);
  }

private:
  ::stepper_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_vel
{
public:
  explicit Init_ControlMessage_input_vel(::stepper_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_torque input_vel(::stepper_can::msg::ControlMessage::_input_vel_type arg)
  {
    msg_.input_vel = std::move(arg);
    return Init_ControlMessage_input_torque(msg_);
  }

private:
  ::stepper_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_pos
{
public:
  explicit Init_ControlMessage_input_pos(::stepper_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_vel input_pos(::stepper_can::msg::ControlMessage::_input_pos_type arg)
  {
    msg_.input_pos = std::move(arg);
    return Init_ControlMessage_input_vel(msg_);
  }

private:
  ::stepper_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_mode
{
public:
  explicit Init_ControlMessage_input_mode(::stepper_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_pos input_mode(::stepper_can::msg::ControlMessage::_input_mode_type arg)
  {
    msg_.input_mode = std::move(arg);
    return Init_ControlMessage_input_pos(msg_);
  }

private:
  ::stepper_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_control_mode
{
public:
  Init_ControlMessage_control_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlMessage_input_mode control_mode(::stepper_can::msg::ControlMessage::_control_mode_type arg)
  {
    msg_.control_mode = std::move(arg);
    return Init_ControlMessage_input_mode(msg_);
  }

private:
  ::stepper_can::msg::ControlMessage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::stepper_can::msg::ControlMessage>()
{
  return stepper_can::msg::builder::Init_ControlMessage_control_mode();
}

}  // namespace stepper_can

#endif  // STEPPER_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
