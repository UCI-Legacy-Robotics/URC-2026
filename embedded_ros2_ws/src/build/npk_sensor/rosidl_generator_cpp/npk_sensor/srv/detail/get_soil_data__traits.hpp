// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice

#ifndef NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__TRAITS_HPP_
#define NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "npk_sensor/srv/detail/get_soil_data__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace npk_sensor
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetSoilData_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetSoilData_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetSoilData_Request & msg, bool use_flow_style = false)
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

}  // namespace npk_sensor

namespace rosidl_generator_traits
{

[[deprecated("use npk_sensor::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const npk_sensor::srv::GetSoilData_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  npk_sensor::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use npk_sensor::srv::to_yaml() instead")]]
inline std::string to_yaml(const npk_sensor::srv::GetSoilData_Request & msg)
{
  return npk_sensor::srv::to_yaml(msg);
}

template<>
inline const char * data_type<npk_sensor::srv::GetSoilData_Request>()
{
  return "npk_sensor::srv::GetSoilData_Request";
}

template<>
inline const char * name<npk_sensor::srv::GetSoilData_Request>()
{
  return "npk_sensor/srv/GetSoilData_Request";
}

template<>
struct has_fixed_size<npk_sensor::srv::GetSoilData_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<npk_sensor::srv::GetSoilData_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<npk_sensor::srv::GetSoilData_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace npk_sensor
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetSoilData_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: ph
  {
    out << "ph: ";
    rosidl_generator_traits::value_to_yaml(msg.ph, out);
    out << ", ";
  }

  // member: moisture
  {
    out << "moisture: ";
    rosidl_generator_traits::value_to_yaml(msg.moisture, out);
    out << ", ";
  }

  // member: temperature
  {
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << ", ";
  }

  // member: conductivity
  {
    out << "conductivity: ";
    rosidl_generator_traits::value_to_yaml(msg.conductivity, out);
    out << ", ";
  }

  // member: nitrogen
  {
    out << "nitrogen: ";
    rosidl_generator_traits::value_to_yaml(msg.nitrogen, out);
    out << ", ";
  }

  // member: phosphorus
  {
    out << "phosphorus: ";
    rosidl_generator_traits::value_to_yaml(msg.phosphorus, out);
    out << ", ";
  }

  // member: potassium
  {
    out << "potassium: ";
    rosidl_generator_traits::value_to_yaml(msg.potassium, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetSoilData_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: ph
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "ph: ";
    rosidl_generator_traits::value_to_yaml(msg.ph, out);
    out << "\n";
  }

  // member: moisture
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "moisture: ";
    rosidl_generator_traits::value_to_yaml(msg.moisture, out);
    out << "\n";
  }

  // member: temperature
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << "\n";
  }

  // member: conductivity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "conductivity: ";
    rosidl_generator_traits::value_to_yaml(msg.conductivity, out);
    out << "\n";
  }

  // member: nitrogen
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "nitrogen: ";
    rosidl_generator_traits::value_to_yaml(msg.nitrogen, out);
    out << "\n";
  }

  // member: phosphorus
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phosphorus: ";
    rosidl_generator_traits::value_to_yaml(msg.phosphorus, out);
    out << "\n";
  }

  // member: potassium
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "potassium: ";
    rosidl_generator_traits::value_to_yaml(msg.potassium, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetSoilData_Response & msg, bool use_flow_style = false)
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

}  // namespace npk_sensor

namespace rosidl_generator_traits
{

[[deprecated("use npk_sensor::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const npk_sensor::srv::GetSoilData_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  npk_sensor::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use npk_sensor::srv::to_yaml() instead")]]
inline std::string to_yaml(const npk_sensor::srv::GetSoilData_Response & msg)
{
  return npk_sensor::srv::to_yaml(msg);
}

template<>
inline const char * data_type<npk_sensor::srv::GetSoilData_Response>()
{
  return "npk_sensor::srv::GetSoilData_Response";
}

template<>
inline const char * name<npk_sensor::srv::GetSoilData_Response>()
{
  return "npk_sensor/srv/GetSoilData_Response";
}

template<>
struct has_fixed_size<npk_sensor::srv::GetSoilData_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<npk_sensor::srv::GetSoilData_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<npk_sensor::srv::GetSoilData_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<npk_sensor::srv::GetSoilData>()
{
  return "npk_sensor::srv::GetSoilData";
}

template<>
inline const char * name<npk_sensor::srv::GetSoilData>()
{
  return "npk_sensor/srv/GetSoilData";
}

template<>
struct has_fixed_size<npk_sensor::srv::GetSoilData>
  : std::integral_constant<
    bool,
    has_fixed_size<npk_sensor::srv::GetSoilData_Request>::value &&
    has_fixed_size<npk_sensor::srv::GetSoilData_Response>::value
  >
{
};

template<>
struct has_bounded_size<npk_sensor::srv::GetSoilData>
  : std::integral_constant<
    bool,
    has_bounded_size<npk_sensor::srv::GetSoilData_Request>::value &&
    has_bounded_size<npk_sensor::srv::GetSoilData_Response>::value
  >
{
};

template<>
struct is_service<npk_sensor::srv::GetSoilData>
  : std::true_type
{
};

template<>
struct is_service_request<npk_sensor::srv::GetSoilData_Request>
  : std::true_type
{
};

template<>
struct is_service_response<npk_sensor::srv::GetSoilData_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__TRAITS_HPP_
