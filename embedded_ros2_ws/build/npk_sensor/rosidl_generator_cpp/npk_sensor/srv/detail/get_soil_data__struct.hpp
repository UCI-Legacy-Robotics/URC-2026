// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice

#ifndef NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__STRUCT_HPP_
#define NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__npk_sensor__srv__GetSoilData_Request __attribute__((deprecated))
#else
# define DEPRECATED__npk_sensor__srv__GetSoilData_Request __declspec(deprecated)
#endif

namespace npk_sensor
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetSoilData_Request_
{
  using Type = GetSoilData_Request_<ContainerAllocator>;

  explicit GetSoilData_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetSoilData_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    npk_sensor::srv::GetSoilData_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const npk_sensor::srv::GetSoilData_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      npk_sensor::srv::GetSoilData_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      npk_sensor::srv::GetSoilData_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__npk_sensor__srv__GetSoilData_Request
    std::shared_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__npk_sensor__srv__GetSoilData_Request
    std::shared_ptr<npk_sensor::srv::GetSoilData_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetSoilData_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetSoilData_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetSoilData_Request_

// alias to use template instance with default allocator
using GetSoilData_Request =
  npk_sensor::srv::GetSoilData_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace npk_sensor


#ifndef _WIN32
# define DEPRECATED__npk_sensor__srv__GetSoilData_Response __attribute__((deprecated))
#else
# define DEPRECATED__npk_sensor__srv__GetSoilData_Response __declspec(deprecated)
#endif

namespace npk_sensor
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetSoilData_Response_
{
  using Type = GetSoilData_Response_<ContainerAllocator>;

  explicit GetSoilData_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->ph = 0.0f;
      this->moisture = 0.0f;
      this->temperature = 0.0f;
      this->conductivity = 0.0f;
      this->nitrogen = 0.0f;
      this->phosphorus = 0.0f;
      this->potassium = 0.0f;
    }
  }

  explicit GetSoilData_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->ph = 0.0f;
      this->moisture = 0.0f;
      this->temperature = 0.0f;
      this->conductivity = 0.0f;
      this->nitrogen = 0.0f;
      this->phosphorus = 0.0f;
      this->potassium = 0.0f;
    }
  }

  // field types and members
  using _ph_type =
    float;
  _ph_type ph;
  using _moisture_type =
    float;
  _moisture_type moisture;
  using _temperature_type =
    float;
  _temperature_type temperature;
  using _conductivity_type =
    float;
  _conductivity_type conductivity;
  using _nitrogen_type =
    float;
  _nitrogen_type nitrogen;
  using _phosphorus_type =
    float;
  _phosphorus_type phosphorus;
  using _potassium_type =
    float;
  _potassium_type potassium;

  // setters for named parameter idiom
  Type & set__ph(
    const float & _arg)
  {
    this->ph = _arg;
    return *this;
  }
  Type & set__moisture(
    const float & _arg)
  {
    this->moisture = _arg;
    return *this;
  }
  Type & set__temperature(
    const float & _arg)
  {
    this->temperature = _arg;
    return *this;
  }
  Type & set__conductivity(
    const float & _arg)
  {
    this->conductivity = _arg;
    return *this;
  }
  Type & set__nitrogen(
    const float & _arg)
  {
    this->nitrogen = _arg;
    return *this;
  }
  Type & set__phosphorus(
    const float & _arg)
  {
    this->phosphorus = _arg;
    return *this;
  }
  Type & set__potassium(
    const float & _arg)
  {
    this->potassium = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    npk_sensor::srv::GetSoilData_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const npk_sensor::srv::GetSoilData_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      npk_sensor::srv::GetSoilData_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      npk_sensor::srv::GetSoilData_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__npk_sensor__srv__GetSoilData_Response
    std::shared_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__npk_sensor__srv__GetSoilData_Response
    std::shared_ptr<npk_sensor::srv::GetSoilData_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetSoilData_Response_ & other) const
  {
    if (this->ph != other.ph) {
      return false;
    }
    if (this->moisture != other.moisture) {
      return false;
    }
    if (this->temperature != other.temperature) {
      return false;
    }
    if (this->conductivity != other.conductivity) {
      return false;
    }
    if (this->nitrogen != other.nitrogen) {
      return false;
    }
    if (this->phosphorus != other.phosphorus) {
      return false;
    }
    if (this->potassium != other.potassium) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetSoilData_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetSoilData_Response_

// alias to use template instance with default allocator
using GetSoilData_Response =
  npk_sensor::srv::GetSoilData_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace npk_sensor

namespace npk_sensor
{

namespace srv
{

struct GetSoilData
{
  using Request = npk_sensor::srv::GetSoilData_Request;
  using Response = npk_sensor::srv::GetSoilData_Response;
};

}  // namespace srv

}  // namespace npk_sensor

#endif  // NPK_SENSOR__SRV__DETAIL__GET_SOIL_DATA__STRUCT_HPP_
