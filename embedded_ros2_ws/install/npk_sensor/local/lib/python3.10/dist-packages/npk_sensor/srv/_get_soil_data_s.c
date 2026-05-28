// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from npk_sensor:srv/GetSoilData.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "npk_sensor/srv/detail/get_soil_data__struct.h"
#include "npk_sensor/srv/detail/get_soil_data__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool npk_sensor__srv__get_soil_data__request__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[50];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("npk_sensor.srv._get_soil_data.GetSoilData_Request", full_classname_dest, 49) == 0);
  }
  npk_sensor__srv__GetSoilData_Request * ros_message = _ros_message;
  ros_message->structure_needs_at_least_one_member = 0;

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * npk_sensor__srv__get_soil_data__request__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of GetSoilData_Request */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("npk_sensor.srv._get_soil_data");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "GetSoilData_Request");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  (void)raw_ros_message;

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// already included above
// #include <Python.h>
// already included above
// #include <stdbool.h>
// already included above
// #include "numpy/ndarrayobject.h"
// already included above
// #include "rosidl_runtime_c/visibility_control.h"
// already included above
// #include "npk_sensor/srv/detail/get_soil_data__struct.h"
// already included above
// #include "npk_sensor/srv/detail/get_soil_data__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool npk_sensor__srv__get_soil_data__response__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[51];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("npk_sensor.srv._get_soil_data.GetSoilData_Response", full_classname_dest, 50) == 0);
  }
  npk_sensor__srv__GetSoilData_Response * ros_message = _ros_message;
  {  // ph
    PyObject * field = PyObject_GetAttrString(_pymsg, "ph");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->ph = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // moisture
    PyObject * field = PyObject_GetAttrString(_pymsg, "moisture");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->moisture = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // temperature
    PyObject * field = PyObject_GetAttrString(_pymsg, "temperature");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->temperature = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // conductivity
    PyObject * field = PyObject_GetAttrString(_pymsg, "conductivity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->conductivity = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // nitrogen
    PyObject * field = PyObject_GetAttrString(_pymsg, "nitrogen");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->nitrogen = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // phosphorus
    PyObject * field = PyObject_GetAttrString(_pymsg, "phosphorus");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->phosphorus = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // potassium
    PyObject * field = PyObject_GetAttrString(_pymsg, "potassium");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->potassium = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * npk_sensor__srv__get_soil_data__response__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of GetSoilData_Response */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("npk_sensor.srv._get_soil_data");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "GetSoilData_Response");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  npk_sensor__srv__GetSoilData_Response * ros_message = (npk_sensor__srv__GetSoilData_Response *)raw_ros_message;
  {  // ph
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->ph);
    {
      int rc = PyObject_SetAttrString(_pymessage, "ph", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // moisture
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->moisture);
    {
      int rc = PyObject_SetAttrString(_pymessage, "moisture", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // temperature
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->temperature);
    {
      int rc = PyObject_SetAttrString(_pymessage, "temperature", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // conductivity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->conductivity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "conductivity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // nitrogen
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->nitrogen);
    {
      int rc = PyObject_SetAttrString(_pymessage, "nitrogen", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // phosphorus
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->phosphorus);
    {
      int rc = PyObject_SetAttrString(_pymessage, "phosphorus", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // potassium
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->potassium);
    {
      int rc = PyObject_SetAttrString(_pymessage, "potassium", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
