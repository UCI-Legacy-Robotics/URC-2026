// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from stepper_can:srv/AxisState.idl
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__SRV__DETAIL__AXIS_STATE__BUILDER_HPP_
#define STEPPER_CAN__SRV__DETAIL__AXIS_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "stepper_can/srv/detail/axis_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace stepper_can
{

namespace srv
{

namespace builder
{

class Init_AxisState_Request_axis_requested_state
{
public:
  Init_AxisState_Request_axis_requested_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::stepper_can::srv::AxisState_Request axis_requested_state(::stepper_can::srv::AxisState_Request::_axis_requested_state_type arg)
  {
    msg_.axis_requested_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::stepper_can::srv::AxisState_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::stepper_can::srv::AxisState_Request>()
{
  return stepper_can::srv::builder::Init_AxisState_Request_axis_requested_state();
}

}  // namespace stepper_can


namespace stepper_can
{

namespace srv
{

namespace builder
{

class Init_AxisState_Response_procedure_result
{
public:
  explicit Init_AxisState_Response_procedure_result(::stepper_can::srv::AxisState_Response & msg)
  : msg_(msg)
  {}
  ::stepper_can::srv::AxisState_Response procedure_result(::stepper_can::srv::AxisState_Response::_procedure_result_type arg)
  {
    msg_.procedure_result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::stepper_can::srv::AxisState_Response msg_;
};

class Init_AxisState_Response_axis_state
{
public:
  explicit Init_AxisState_Response_axis_state(::stepper_can::srv::AxisState_Response & msg)
  : msg_(msg)
  {}
  Init_AxisState_Response_procedure_result axis_state(::stepper_can::srv::AxisState_Response::_axis_state_type arg)
  {
    msg_.axis_state = std::move(arg);
    return Init_AxisState_Response_procedure_result(msg_);
  }

private:
  ::stepper_can::srv::AxisState_Response msg_;
};

class Init_AxisState_Response_active_errors
{
public:
  Init_AxisState_Response_active_errors()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AxisState_Response_axis_state active_errors(::stepper_can::srv::AxisState_Response::_active_errors_type arg)
  {
    msg_.active_errors = std::move(arg);
    return Init_AxisState_Response_axis_state(msg_);
  }

private:
  ::stepper_can::srv::AxisState_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::stepper_can::srv::AxisState_Response>()
{
  return stepper_can::srv::builder::Init_AxisState_Response_active_errors();
}

}  // namespace stepper_can

#endif  // STEPPER_CAN__SRV__DETAIL__AXIS_STATE__BUILDER_HPP_
