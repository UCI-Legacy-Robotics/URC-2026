// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drive_teleop:msg/DriveControlMessage.idl
// generated code does not contain a copyright notice

#ifndef DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__TRAITS_HPP_
#define DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "drive_teleop/msg/detail/drive_control_message__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace drive_teleop
{

namespace msg
{

inline void to_flow_style_yaml(
  const DriveControlMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: left_input_pwm
  {
    out << "left_input_pwm: ";
    rosidl_generator_traits::value_to_yaml(msg.left_input_pwm, out);
    out << ", ";
  }

  // member: right_input_pwm
  {
    out << "right_input_pwm: ";
    rosidl_generator_traits::value_to_yaml(msg.right_input_pwm, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DriveControlMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: left_input_pwm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_input_pwm: ";
    rosidl_generator_traits::value_to_yaml(msg.left_input_pwm, out);
    out << "\n";
  }

  // member: right_input_pwm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_input_pwm: ";
    rosidl_generator_traits::value_to_yaml(msg.right_input_pwm, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DriveControlMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace drive_teleop

namespace rosidl_generator_traits
{

[[deprecated("use drive_teleop::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drive_teleop::msg::DriveControlMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  drive_teleop::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drive_teleop::msg::to_yaml() instead")]]
inline std::string to_yaml(const drive_teleop::msg::DriveControlMessage & msg)
{
  return drive_teleop::msg::to_yaml(msg);
}

template<>
inline const char * data_type<drive_teleop::msg::DriveControlMessage>()
{
  return "drive_teleop::msg::DriveControlMessage";
}

template<>
inline const char * name<drive_teleop::msg::DriveControlMessage>()
{
  return "drive_teleop/msg/DriveControlMessage";
}

template<>
struct has_fixed_size<drive_teleop::msg::DriveControlMessage>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<drive_teleop::msg::DriveControlMessage>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<drive_teleop::msg::DriveControlMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DRIVE_TELEOP__MSG__DETAIL__DRIVE_CONTROL_MESSAGE__TRAITS_HPP_
