"""
Validator schemas for the data received
"""
from datetime import datetime
from collections import namedtuple
from cerberus import Validator


SCHEMA_NAMES = namedtuple('SCHEMA_NAMES', 'sensor_data')

schema_names = SCHEMA_NAMES(
    sensor_data='sensor_data_schema',
)

schemas = {
    'sensor_data_schema': {
        'id': {'required': True, 'type': 'string'},
        'payload': {'required': True, 'type': 'integer'},
        'datetime': {
            'isdatetime': True, 'type': 'string', 'required': True, 'nullable': False
        }
    }
}


class ExtendedValidator(Validator):
    """
    Extended validator class with custom validation and conversion if needed
    """
    def _validate_isdatetime(self, isdatetime, field, value):
        """
        Validation for datetime field. Expecting it match the pattern %Y%m%dT%H%M
        :param isdatetime: Does it needs to be validated
        :type isdatetime: bool
        :param field: field in self.document object returned after validation
        :type field: str
        :param value: received value
        :type value: str
        """
        if isdatetime:
            try:
                datetime.strptime(value, '%Y%m%dT%H%M')
            except ValueError:
                self._error(field, 'Datetime field must be of format %Y%m%dT%H%M')

    # def _normalize_coerce_custom_datetime(self, value):
    #     """
    #     :param value: value to be converted
    #     :type value: str
    #     :rtype datetime
    #     """
    #     return datetime.strptime(value, '%Y%m%dT%H%M')


class RequestValidator:
    """
    Request validator class
    """
    def __init__(self):
        pass

    @staticmethod
    def data_validator(data, validation_schema):
        """
        Validates data received
        :param data: data to be validated
        :type data: dict || str
        :param validation_schema: schema to be used for validation
        :type validation_schema: str
        :rtype: bool || dict
        """
        validator = ExtendedValidator()
        if not validator.validate(data, schemas.get(validation_schema)):
            return {'status': False, 'errors': validator.errors}
        return {'status': True, 'document': validator.document}
