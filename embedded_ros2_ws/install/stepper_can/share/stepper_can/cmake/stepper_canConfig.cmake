# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_stepper_can_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED stepper_can_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(stepper_can_FOUND FALSE)
  elseif(NOT stepper_can_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(stepper_can_FOUND FALSE)
  endif()
  return()
endif()
set(_stepper_can_CONFIG_INCLUDED TRUE)

# output package information
if(NOT stepper_can_FIND_QUIETLY)
  message(STATUS "Found stepper_can: 0.0.1 (${stepper_can_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'stepper_can' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${stepper_can_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(stepper_can_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "rosidl_cmake-extras.cmake;ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_libraries-extras.cmake;ament_cmake_export_targets-extras.cmake;rosidl_cmake_export_typesupport_targets-extras.cmake;ament_cmake_export_dependencies-extras.cmake;rosidl_cmake_export_typesupport_libraries-extras.cmake")
foreach(_extra ${_extras})
  include("${stepper_can_DIR}/${_extra}")
endforeach()
