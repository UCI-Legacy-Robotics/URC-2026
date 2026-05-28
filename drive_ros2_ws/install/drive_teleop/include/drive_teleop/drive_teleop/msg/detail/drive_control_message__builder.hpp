// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice

#ifndef DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__BUILDER_HPP_
#define DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drive_teleop/msg/detail/drive_control_message__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drive_teleop
{

namespace msg
{

namespace builder
{

class Init_DriveControlMessage_right_input_pwm
{
public:
  explicit Init_DriveControlMessage_right_input_pwm(::drive_teleop::msg::DriveControlMessage & msg)
  : msg_(msg)
  {}
  ::drive_teleop::msg::DriveControlMessage right_input_pwm(::drive_teleop::msg::DriveControlMessage::_right_input_pwm_type arg)
  {
    msg_.right_input_pwm = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drive_teleop::msg::DriveControlMessage msg_;
};

class Init_DriveControlMessage_left_input_pwm
{
public:
  explicit Init_DriveControlMessage_left_input_pwm(::drive_teleop::msg::DriveControlMessage & msg)
  : msg_(msg)
  {}
  Init_DriveControlMessage_right_input_pwm left_input_pwm(::drive_teleop::msg::DriveControlMessage::_left_input_pwm_type arg)
  {
    msg_.left_input_pwm = std::move(arg);
    return Init_DriveControlMessage_right_input_pwm(msg_);
  }

private:
  ::drive_teleop::msg::DriveControlMessage msg_;
};

class Init_DriveControlMessage_header
{
public:
  Init_DriveControlMessage_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DriveControlMessage_left_input_pwm header(::drive_teleop::msg::DriveControlMessage::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_DriveControlMessage_left_input_pwm(msg_);
  }

private:
  ::drive_teleop::msg::DriveControlMessage msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drive_teleop::msg::DriveControlMessage>()
{
  return drive_teleop::msg::builder::Init_DriveControlMessage_header();
}

}  // namespace drive_teleop

#endif  // DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__BUILDER_HPP_
