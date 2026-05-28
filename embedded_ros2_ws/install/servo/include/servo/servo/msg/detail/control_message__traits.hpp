// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from servo:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef SERVO__MSG__DETAIL__CONTROL_MESSAGE__TRAITS_HPP_
#define SERVO__MSG__DETAIL__CONTROL_MESSAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "servo/msg/detail/control_message__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace servo
{

namespace msg
{

inline void to_flow_style_yaml(
  const ControlMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: control_mode
  {
    out << "control_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.control_mode, out);
    out << ", ";
  }

  // member: input_vel_deg
  {
    out << "input_vel_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.input_vel_deg, out);
    out << ", ";
  }

  // member: input_pos_deg
  {
    out << "input_pos_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.input_pos_deg, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ControlMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: control_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "control_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.control_mode, out);
    out << "\n";
  }

  // member: input_vel_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "input_vel_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.input_vel_deg, out);
    out << "\n";
  }

  // member: input_pos_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "input_pos_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.input_pos_deg, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ControlMessage & msg, bool use_flow_style = false)
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

}  // namespace servo

namespace rosidl_generator_traits
{

[[deprecated("use servo::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const servo::msg::ControlMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  servo::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use servo::msg::to_yaml() instead")]]
inline std::string to_yaml(const servo::msg::ControlMessage & msg)
{
  return servo::msg::to_yaml(msg);
}

template<>
inline const char * data_type<servo::msg::ControlMessage>()
{
  return "servo::msg::ControlMessage";
}

template<>
inline const char * name<servo::msg::ControlMessage>()
{
  return "servo/msg/ControlMessage";
}

template<>
struct has_fixed_size<servo::msg::ControlMessage>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<servo::msg::ControlMessage>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<servo::msg::ControlMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SERVO__MSG__DETAIL__CONTROL_MESSAGE__TRAITS_HPP_
