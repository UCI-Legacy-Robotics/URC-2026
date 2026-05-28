// generated from rosidl_generator_cpp/resource/rosidl_generator_cpp__visibility_control.hpp.in
// generated code does not contain a copyright notice

#ifndef STEPPER_CAN__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_
#define STEPPER_CAN__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_GENERATOR_CPP_EXPORT_stepper_can __attribute__ ((dllexport))
    #define ROSIDL_GENERATOR_CPP_IMPORT_stepper_can __attribute__ ((dllimport))
  #else
    #define ROSIDL_GENERATOR_CPP_EXPORT_stepper_can __declspec(dllexport)
    #define ROSIDL_GENERATOR_CPP_IMPORT_stepper_can __declspec(dllimport)
  #endif
  #ifdef ROSIDL_GENERATOR_CPP_BUILDING_DLL_stepper_can
    #define ROSIDL_GENERATOR_CPP_PUBLIC_stepper_can ROSIDL_GENERATOR_CPP_EXPORT_stepper_can
  #else
    #define ROSIDL_GENERATOR_CPP_PUBLIC_stepper_can ROSIDL_GENERATOR_CPP_IMPORT_stepper_can
  #endif
#else
  #define ROSIDL_GENERATOR_CPP_EXPORT_stepper_can __attribute__ ((visibility("default")))
  #define ROSIDL_GENERATOR_CPP_IMPORT_stepper_can
  #if __GNUC__ >= 4
    #define ROSIDL_GENERATOR_CPP_PUBLIC_stepper_can __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_GENERATOR_CPP_PUBLIC_stepper_can
  #endif
#endif

#ifdef __cplusplus
}
#endif

#endif  // STEPPER_CAN__MSG__ROSIDL_GENERATOR_CPP__VISIBILITY_CONTROL_HPP_
