// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from yellowjacket_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef YELLOWJACKET_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
#define YELLOWJACKET_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "yellowjacket_can/msg/detail/control_message__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace yellowjacket_can
{

namespace msg
{

namespace builder
{

class Init_ControlMessage_input_torque
{
public:
  explicit Init_ControlMessage_input_torque(::yellowjacket_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  ::yellowjacket_can::msg::ControlMessage input_torque(::yellowjacket_can::msg::ControlMessage::_input_torque_type arg)
  {
    msg_.input_torque = std::move(arg);
    return std::move(msg_);
  }

private:
  ::yellowjacket_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_vel
{
public:
  explicit Init_ControlMessage_input_vel(::yellowjacket_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_torque input_vel(::yellowjacket_can::msg::ControlMessage::_input_vel_type arg)
  {
    msg_.input_vel = std::move(arg);
    return Init_ControlMessage_input_torque(msg_);
  }

private:
  ::yellowjacket_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_pos
{
public:
  explicit Init_ControlMessage_input_pos(::yellowjacket_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_vel input_pos(::yellowjacket_can::msg::ControlMessage::_input_pos_type arg)
  {
    msg_.input_pos = std::move(arg);
    return Init_ControlMessage_input_vel(msg_);
  }

private:
  ::yellowjacket_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_input_mode
{
public:
  explicit Init_ControlMessage_input_mode(::yellowjacket_can::msg::ControlMessage & msg)
  : msg_(msg)
  {}
  Init_ControlMessage_input_pos input_mode(::yellowjacket_can::msg::ControlMessage::_input_mode_type arg)
  {
    msg_.input_mode = std::move(arg);
    return Init_ControlMessage_input_pos(msg_);
  }

private:
  ::yellowjacket_can::msg::ControlMessage msg_;
};

class Init_ControlMessage_control_mode
{
public:
  Init_ControlMessage_control_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlMessage_input_mode control_mode(::yellowjacket_can::msg::ControlMessage::_control_mode_type arg)
  {
    msg_.control_mode = std::move(arg);
    return Init_ControlMessage_input_mode(msg_);
  }

private:
  ::yellowjacket_can::msg::ControlMessage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::yellowjacket_can::msg::ControlMessage>()
{
  return yellowjacket_can::msg::builder::Init_ControlMessage_control_mode();
}

}  // namespace yellowjacket_can

#endif  // YELLOWJACKET_CAN__MSG__DETAIL__CONTROL_MESSAGE__BUILDER_HPP_
