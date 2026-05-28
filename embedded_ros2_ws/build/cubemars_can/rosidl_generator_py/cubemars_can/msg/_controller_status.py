# generated from rosidl_generator_py/resource/_idl.py.em
# with input from cubemars_can:msg/ControllerStatus.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ControllerStatus(type):
    """Metaclass of message 'ControllerStatus'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('cubemars_can')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'cubemars_can.msg.ControllerStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__controller_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__controller_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__controller_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__controller_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__controller_status

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ControllerStatus(metaclass=Metaclass_ControllerStatus):
    """Message class 'ControllerStatus'."""

    __slots__ = [
        '_pos_estimate_deg',
        '_vel_estimate_rpm',
        '_motor_current_amps',
        '_motor_temperature_c',
        '_active_errors',
    ]

    _fields_and_field_types = {
        'pos_estimate_deg': 'float',
        'vel_estimate_rpm': 'float',
        'motor_current_amps': 'float',
        'motor_temperature_c': 'int8',
        'active_errors': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.pos_estimate_deg = kwargs.get('pos_estimate_deg', float())
        self.vel_estimate_rpm = kwargs.get('vel_estimate_rpm', float())
        self.motor_current_amps = kwargs.get('motor_current_amps', float())
        self.motor_temperature_c = kwargs.get('motor_temperature_c', int())
        self.active_errors = kwargs.get('active_errors', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.pos_estimate_deg != other.pos_estimate_deg:
            return False
        if self.vel_estimate_rpm != other.vel_estimate_rpm:
            return False
        if self.motor_current_amps != other.motor_current_amps:
            return False
        if self.motor_temperature_c != other.motor_temperature_c:
            return False
        if self.active_errors != other.active_errors:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def pos_estimate_deg(self):
        """Message field 'pos_estimate_deg'."""
        return self._pos_estimate_deg

    @pos_estimate_deg.setter
    def pos_estimate_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'pos_estimate_deg' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'pos_estimate_deg' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._pos_estimate_deg = value

    @builtins.property
    def vel_estimate_rpm(self):
        """Message field 'vel_estimate_rpm'."""
        return self._vel_estimate_rpm

    @vel_estimate_rpm.setter
    def vel_estimate_rpm(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'vel_estimate_rpm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'vel_estimate_rpm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._vel_estimate_rpm = value

    @builtins.property
    def motor_current_amps(self):
        """Message field 'motor_current_amps'."""
        return self._motor_current_amps

    @motor_current_amps.setter
    def motor_current_amps(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'motor_current_amps' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'motor_current_amps' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._motor_current_amps = value

    @builtins.property
    def motor_temperature_c(self):
        """Message field 'motor_temperature_c'."""
        return self._motor_temperature_c

    @motor_temperature_c.setter
    def motor_temperature_c(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'motor_temperature_c' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'motor_temperature_c' field must be an integer in [-128, 127]"
        self._motor_temperature_c = value

    @builtins.property
    def active_errors(self):
        """Message field 'active_errors'."""
        return self._active_errors

    @active_errors.setter
    def active_errors(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'active_errors' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'active_errors' field must be an unsigned integer in [0, 255]"
        self._active_errors = value
