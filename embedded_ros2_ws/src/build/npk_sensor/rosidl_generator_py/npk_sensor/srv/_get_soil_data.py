# generated from rosidl_generator_py/resource/_idl.py.em
# with input from npk_sensor:srv/GetSoilData.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetSoilData_Request(type):
    """Metaclass of message 'GetSoilData_Request'."""

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
            module = import_type_support('npk_sensor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'npk_sensor.srv.GetSoilData_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_soil_data__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_soil_data__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_soil_data__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_soil_data__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_soil_data__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetSoilData_Request(metaclass=Metaclass_GetSoilData_Request):
    """Message class 'GetSoilData_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

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
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetSoilData_Response(type):
    """Metaclass of message 'GetSoilData_Response'."""

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
            module = import_type_support('npk_sensor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'npk_sensor.srv.GetSoilData_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_soil_data__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_soil_data__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_soil_data__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_soil_data__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_soil_data__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetSoilData_Response(metaclass=Metaclass_GetSoilData_Response):
    """Message class 'GetSoilData_Response'."""

    __slots__ = [
        '_ph',
        '_moisture',
        '_temperature',
        '_conductivity',
        '_nitrogen',
        '_phosphorus',
        '_potassium',
    ]

    _fields_and_field_types = {
        'ph': 'float',
        'moisture': 'float',
        'temperature': 'float',
        'conductivity': 'float',
        'nitrogen': 'float',
        'phosphorus': 'float',
        'potassium': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.ph = kwargs.get('ph', float())
        self.moisture = kwargs.get('moisture', float())
        self.temperature = kwargs.get('temperature', float())
        self.conductivity = kwargs.get('conductivity', float())
        self.nitrogen = kwargs.get('nitrogen', float())
        self.phosphorus = kwargs.get('phosphorus', float())
        self.potassium = kwargs.get('potassium', float())

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
        if self.ph != other.ph:
            return False
        if self.moisture != other.moisture:
            return False
        if self.temperature != other.temperature:
            return False
        if self.conductivity != other.conductivity:
            return False
        if self.nitrogen != other.nitrogen:
            return False
        if self.phosphorus != other.phosphorus:
            return False
        if self.potassium != other.potassium:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def ph(self):
        """Message field 'ph'."""
        return self._ph

    @ph.setter
    def ph(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'ph' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'ph' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._ph = value

    @builtins.property
    def moisture(self):
        """Message field 'moisture'."""
        return self._moisture

    @moisture.setter
    def moisture(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'moisture' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'moisture' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._moisture = value

    @builtins.property
    def temperature(self):
        """Message field 'temperature'."""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'temperature' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'temperature' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._temperature = value

    @builtins.property
    def conductivity(self):
        """Message field 'conductivity'."""
        return self._conductivity

    @conductivity.setter
    def conductivity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'conductivity' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'conductivity' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._conductivity = value

    @builtins.property
    def nitrogen(self):
        """Message field 'nitrogen'."""
        return self._nitrogen

    @nitrogen.setter
    def nitrogen(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'nitrogen' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'nitrogen' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._nitrogen = value

    @builtins.property
    def phosphorus(self):
        """Message field 'phosphorus'."""
        return self._phosphorus

    @phosphorus.setter
    def phosphorus(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'phosphorus' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'phosphorus' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._phosphorus = value

    @builtins.property
    def potassium(self):
        """Message field 'potassium'."""
        return self._potassium

    @potassium.setter
    def potassium(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'potassium' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'potassium' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._potassium = value


class Metaclass_GetSoilData(type):
    """Metaclass of service 'GetSoilData'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('npk_sensor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'npk_sensor.srv.GetSoilData')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_soil_data

            from npk_sensor.srv import _get_soil_data
            if _get_soil_data.Metaclass_GetSoilData_Request._TYPE_SUPPORT is None:
                _get_soil_data.Metaclass_GetSoilData_Request.__import_type_support__()
            if _get_soil_data.Metaclass_GetSoilData_Response._TYPE_SUPPORT is None:
                _get_soil_data.Metaclass_GetSoilData_Response.__import_type_support__()


class GetSoilData(metaclass=Metaclass_GetSoilData):
    from npk_sensor.srv._get_soil_data import GetSoilData_Request as Request
    from npk_sensor.srv._get_soil_data import GetSoilData_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
