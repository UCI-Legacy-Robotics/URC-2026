// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from cubemars_can:msg/ControllerStatus.idl
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__TRAITS_HPP_
#define CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "cubemars_can/msg/detail/controller_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace cubemars_can
{

namespace msg
{

inline void to_flow_style_yaml(
  const ControllerStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: pos_estimate_deg
  {
    out << "pos_estimate_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pos_estimate_deg, out);
    out << ", ";
  }

  // member: vel_estimate_rpm
  {
    out << "vel_estimate_rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.vel_estimate_rpm, out);
    out << ", ";
  }

  // member: motor_current_amps
  {
    out << "motor_current_amps: ";
    rosidl_generator_traits::value_to_yaml(msg.motor_current_amps, out);
    out << ", ";
  }

  // member: motor_temperature_c
  {
    out << "motor_temperature_c: ";
    rosidl_generator_traits::value_to_yaml(msg.motor_temperature_c, out);
    out << ", ";
  }

  // member: active_errors
  {
    out << "active_errors: ";
    rosidl_generator_traits::value_to_yaml(msg.active_errors, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ControllerStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pos_estimate_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pos_estimate_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pos_estimate_deg, out);
    out << "\n";
  }

  // member: vel_estimate_rpm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vel_estimate_rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.vel_estimate_rpm, out);
    out << "\n";
  }

  // member: motor_current_amps
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "motor_current_amps: ";
    rosidl_generator_traits::value_to_yaml(msg.motor_current_amps, out);
    out << "\n";
  }

  // member: motor_temperature_c
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "motor_temperature_c: ";
    rosidl_generator_traits::value_to_yaml(msg.motor_temperature_c, out);
    out << "\n";
  }

  // member: active_errors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "active_errors: ";
    rosidl_generator_traits::value_to_yaml(msg.active_errors, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ControllerStatus & msg, bool use_flow_style = false)
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
  const cubemars_can::msg::ControllerStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  cubemars_can::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use cubemars_can::msg::to_yaml() instead")]]
inline std::string to_yaml(const cubemars_can::msg::ControllerStatus & msg)
{
  return cubemars_can::msg::to_yaml(msg);
}

template<>
inline const char * data_type<cubemars_can::msg::ControllerStatus>()
{
  return "cubemars_can::msg::ControllerStatus";
}

template<>
inline const char * name<cubemars_can::msg::ControllerStatus>()
{
  return "cubemars_can/msg/ControllerStatus";
}

template<>
struct has_fixed_size<cubemars_can::msg::ControllerStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<cubemars_can::msg::ControllerStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<cubemars_can::msg::ControllerStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUBEMARS_CAN__MSG__DETAIL__CONTROLLER_STATUS__TRAITS_HPP_
