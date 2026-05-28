# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_mock_gps_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED mock_gps_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(mock_gps_FOUND FALSE)
  elseif(NOT mock_gps_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(mock_gps_FOUND FALSE)
  endif()
  return()
endif()
set(_mock_gps_CONFIG_INCLUDED TRUE)

# output package information
if(NOT mock_gps_FIND_QUIETLY)
  message(STATUS "Found mock_gps: 0.0.0 (${mock_gps_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'mock_gps' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${mock_gps_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(mock_gps_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${mock_gps_DIR}/${_extra}")
endforeach()
