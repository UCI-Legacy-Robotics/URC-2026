// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice

#ifndef NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__BUILDER_HPP_
#define NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "npk_sensor/srv/detail/get_soil_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace npk_sensor
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::npk_sensor::srv::GetSoilData_Request>()
{
  return ::npk_sensor::srv::GetSoilData_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace npk_sensor


namespace npk_sensor
{

namespace srv
{

namespace builder
{

class Init_GetSoilData_Response_potassium
{
public:
  explicit Init_GetSoilData_Response_potassium(::npk_sensor::srv::GetSoilData_Response & msg)
  : msg_(msg)
  {}
  ::npk_sensor::srv::GetSoilData_Response potassium(::npk_sensor::srv::GetSoilData_Response::_potassium_type arg)
  {
    msg_.potassium = std::move(arg);
    return std::move(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

class Init_GetSoilData_Response_phosphorus
{
public:
  explicit Init_GetSoilData_Response_phosphorus(::npk_sensor::srv::GetSoilData_Response & msg)
  : msg_(msg)
  {}
  Init_GetSoilData_Response_potassium phosphorus(::npk_sensor::srv::GetSoilData_Response::_phosphorus_type arg)
  {
    msg_.phosphorus = std::move(arg);
    return Init_GetSoilData_Response_potassium(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

class Init_GetSoilData_Response_nitrogen
{
public:
  explicit Init_GetSoilData_Response_nitrogen(::npk_sensor::srv::GetSoilData_Response & msg)
  : msg_(msg)
  {}
  Init_GetSoilData_Response_phosphorus nitrogen(::npk_sensor::srv::GetSoilData_Response::_nitrogen_type arg)
  {
    msg_.nitrogen = std::move(arg);
    return Init_GetSoilData_Response_phosphorus(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

class Init_GetSoilData_Response_conductivity
{
public:
  explicit Init_GetSoilData_Response_conductivity(::npk_sensor::srv::GetSoilData_Response & msg)
  : msg_(msg)
  {}
  Init_GetSoilData_Response_nitrogen conductivity(::npk_sensor::srv::GetSoilData_Response::_conductivity_type arg)
  {
    msg_.conductivity = std::move(arg);
    return Init_GetSoilData_Response_nitrogen(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

class Init_GetSoilData_Response_temperature
{
public:
  explicit Init_GetSoilData_Response_temperature(::npk_sensor::srv::GetSoilData_Response & msg)
  : msg_(msg)
  {}
  Init_GetSoilData_Response_conductivity temperature(::npk_sensor::srv::GetSoilData_Response::_temperature_type arg)
  {
    msg_.temperature = std::move(arg);
    return Init_GetSoilData_Response_conductivity(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

class Init_GetSoilData_Response_moisture
{
public:
  explicit Init_GetSoilData_Response_moisture(::npk_sensor::srv::GetSoilData_Response & msg)
  : msg_(msg)
  {}
  Init_GetSoilData_Response_temperature moisture(::npk_sensor::srv::GetSoilData_Response::_moisture_type arg)
  {
    msg_.moisture = std::move(arg);
    return Init_GetSoilData_Response_temperature(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

class Init_GetSoilData_Response_ph
{
public:
  Init_GetSoilData_Response_ph()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetSoilData_Response_moisture ph(::npk_sensor::srv::GetSoilData_Response::_ph_type arg)
  {
    msg_.ph = std::move(arg);
    return Init_GetSoilData_Response_moisture(msg_);
  }

private:
  ::npk_sensor::srv::GetSoilData_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::npk_sensor::srv::GetSoilData_Response>()
{
  return npk_sensor::srv::builder::Init_GetSoilData_Response_ph();
}

}  // namespace npk_sensor

#endif  // NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__BUILDER_HPP_
