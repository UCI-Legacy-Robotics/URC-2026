// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from cubemars_can:msg/ControlMessage.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__TRAITS_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "cubemars_can/msg/detail/control_message__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace cubemars_can
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

  // member: input_vel_rpm
  {
    out << "input_vel_rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.input_vel_rpm, out);
    out << ", ";
  }

  // member: input_pos_deg
  {
    out << "input_pos_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.input_pos_deg, out);
    out << ", ";
  }

  // member: set_vel_limit_rpm
  {
    out << "set_vel_limit_rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.set_vel_limit_rpm, out);
    out << ", ";
  }

  // member: set_accel_limit_rpm_s
  {
    out << "set_accel_limit_rpm_s: ";
    rosidl_generator_traits::value_to_yaml(msg.set_accel_limit_rpm_s, out);
    out << ", ";
  }

  // member: set_origin
  {
    out << "set_origin: ";
    rosidl_generator_traits::value_to_yaml(msg.set_origin, out);
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

  // member: input_vel_rpm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "input_vel_rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.input_vel_rpm, out);
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

  // member: set_vel_limit_rpm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "set_vel_limit_rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.set_vel_limit_rpm, out);
    out << "\n";
  }

  // member: set_accel_limit_rpm_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "set_accel_limit_rpm_s: ";
    rosidl_generator_traits::value_to_yaml(msg.set_accel_limit_rpm_s, out);
    out << "\n";
  }

  // member: set_origin
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "set_origin: ";
    rosidl_generator_traits::value_to_yaml(msg.set_origin, out);
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

}  // namespace cubemars_can

namespace rosidl_generator_traits
{

[[deprecated("use cubemars_can::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const cubemars_can::msg::ControlMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  cubemars_can::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use cubemars_can::msg::to_yaml() instead")]]
inline std::string to_yaml(const cubemars_can::msg::ControlMessage & msg)
{
  return cubemars_can::msg::to_yaml(msg);
}

template<>
inline const char * data_type<cubemars_can::msg::ControlMessage>()
{
  return "cubemars_can::msg::ControlMessage";
}

template<>
inline const char * name<cubemars_can::msg::ControlMessage>()
{
  return "cubemars_can/msg/ControlMessage";
}

template<>
struct has_fixed_size<cubemars_can::msg::ControlMessage>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<cubemars_can::msg::ControlMessage>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<cubemars_can::msg::ControlMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROL_MESSAGE__TRAITS_HPP_
