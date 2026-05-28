// generated from rosidl_generator_c/resource/rosidl_generator_c__visibility_control.h.in
// generated code does not contain a copyright notice

#ifndef CUBEMARS_CAN__MSG__ROSIDL_GENERATOR_C__VISIBILITY_CONTROL_H_
#define CUBEMARS_CAN__MSG__ROSIDL_GENERATOR_C__VISIBILITY_CONTROL_H_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_GENERATOR_C_EXPORT_cubemars_can __attribute__ ((dllexport))
    #define ROSIDL_GENERATOR_C_IMPORT_cubemars_can __attribute__ ((dllimport))
  #else
    #define ROSIDL_GENERATOR_C_EXPORT_cubemars_can __declspec(dllexport)
    #define ROSIDL_GENERATOR_C_IMPORT_cubemars_can __declspec(dllimport)
  #endif
  #ifdef ROSIDL_GENERATOR_C_BUILDING_DLL_cubemars_can
    #define ROSIDL_GENERATOR_C_PUBLIC_cubemars_can ROSIDL_GENERATOR_C_EXPORT_cubemars_can
  #else
    #define ROSIDL_GENERATOR_C_PUBLIC_cubemars_can ROSIDL_GENERATOR_C_IMPORT_cubemars_can
  #endif
#else
  #define ROSIDL_GENERATOR_C_EXPORT_cubemars_can __attribute__ ((visibility("default")))
  #define ROSIDL_GENERATOR_C_IMPORT_cubemars_can
  #if __GNUC__ >= 4
    #define ROSIDL_GENERATOR_C_PUBLIC_cubemars_can __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_GENERATOR_C_PUBLIC_cubemars_can
  #endif
#endif

#ifdef __cplusplus
}
#endif

#endif  // CUBEMARS_CAN__MSG__ROSIDL_GENERATOR_C__VISIBILITY_CONTROL_H_
