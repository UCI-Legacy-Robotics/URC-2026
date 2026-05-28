// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from stepper_can:srv/AxisState.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__SRV__DETAIL__AXIS_STATE__TRAITS_HPP_
#define STEPPER_CAN__SRV__DETAIL__AXIS_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "stepper_can/srv/detail/axis_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace stepper_can
{

namespace srv
{

inline void to_flow_style_yaml(
  const AxisState_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: axis_requested_state
  {
    out << "axis_requested_state: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_requested_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AxisState_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: axis_requested_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "axis_requested_state: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_requested_state, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AxisState_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace stepper_can

namespace rosidl_generator_traits
{

[[deprecated("use stepper_can::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const stepper_can::srv::AxisState_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  stepper_can::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use stepper_can::srv::to_yaml() instead")]]
inline std::string to_yaml(const stepper_can::srv::AxisState_Request & msg)
{
  return stepper_can::srv::to_yaml(msg);
}

template<>
inline const char * data_type<stepper_can::srv::AxisState_Request>()
{
  return "stepper_can::srv::AxisState_Request";
}

template<>
inline const char * name<stepper_can::srv::AxisState_Request>()
{
  return "stepper_can/srv/AxisState_Request";
}

template<>
struct has_fixed_size<stepper_can::srv::AxisState_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<stepper_can::srv::AxisState_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<stepper_can::srv::AxisState_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace stepper_can
{

namespace srv
{

inline void to_flow_style_yaml(
  const AxisState_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: active_errors
  {
    out << "active_errors: ";
    rosidl_generator_traits::value_to_yaml(msg.active_errors, out);
    out << ", ";
  }

  // member: axis_state
  {
    out << "axis_state: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_state, out);
    out << ", ";
  }

  // member: procedure_result
  {
    out << "procedure_result: ";
    rosidl_generator_traits::value_to_yaml(msg.procedure_result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AxisState_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: active_errors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "active_errors: ";
    rosidl_generator_traits::value_to_yaml(msg.active_errors, out);
    out << "\n";
  }

  // member: axis_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "axis_state: ";
    rosidl_generator_traits::value_to_yaml(msg.axis_state, out);
    out << "\n";
  }

  // member: procedure_result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "procedure_result: ";
    rosidl_generator_traits::value_to_yaml(msg.procedure_result, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AxisState_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace stepper_can

namespace rosidl_generator_traits
{

[[deprecated("use stepper_can::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const stepper_can::srv::AxisState_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  stepper_can::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use stepper_can::srv::to_yaml() instead")]]
inline std::string to_yaml(const stepper_can::srv::AxisState_Response & msg)
{
  return stepper_can::srv::to_yaml(msg);
}

template<>
inline const char * data_type<stepper_can::srv::AxisState_Response>()
{
  return "stepper_can::srv::AxisState_Response";
}

template<>
inline const char * name<stepper_can::srv::AxisState_Response>()
{
  return "stepper_can/srv/AxisState_Response";
}

template<>
struct has_fixed_size<stepper_can::srv::AxisState_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<stepper_can::srv::AxisState_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<stepper_can::srv::AxisState_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<stepper_can::srv::AxisState>()
{
  return "stepper_can::srv::AxisState";
}

template<>
inline const char * name<stepper_can::srv::AxisState>()
{
  return "stepper_can/srv/AxisState";
}

template<>
struct has_fixed_size<stepper_can::srv::AxisState>
  : std::integral_constant<
    bool,
    has_fixed_size<stepper_can::srv::AxisState_Request>::value &&
    has_fixed_size<stepper_can::srv::AxisState_Response>::value
  >
{
};

template<>
struct has_bounded_size<stepper_can::srv::AxisState>
  : std::integral_constant<
    bool,
    has_bounded_size<stepper_can::srv::AxisState_Request>::value &&
    has_bounded_size<stepper_can::srv::AxisState_Response>::value
  >
{
};

template<>
struct is_service<stepper_can::srv::AxisState>
  : std::true_type
{
};

template<>
struct is_service_request<stepper_can::srv::AxisState_Request>
  : std::true_type
{
};

template<>
struct is_service_response<stepper_can::srv::AxisState_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // STEPPER_CAN__SRV__DETAIL__AXIS_STATE__TRAITS_HPP_
