"""
Tests for validators.py schemas
"""
from unittest import TestCase

from controller_app.validators import schema_names, RequestValidator


class TestValidators(TestCase):

    def setUp(self):
        pass

    def test_fail_validate_datetime(self):
        """
        Testing wrongly crafted datetime field
        """
        data = [
            {'payload': 2, 'datetime': '129'},
            {'payload': 2, 'datetime': '20190201R0935'},
            {'payload': 2, 'datetime': '20190201T2935'},
            {'payload': 2, 'datetime': '00190201Tw'},
            {'payload': 2, 'datetime': '20191301T00'},
            {'payload': 2, 'datetime': '201999T2935'},
            {'payload': 2, 'datetime': '20190101T2935'},
            {'payload': 2, 'datetime': '2019101T121212'},
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertFalse(result['status'])

    def test_pass_validate_datetime(self):
        """
        Testing well crafted datetime field
        """
        data = [
            {'payload': 2, 'datetime': '20190201T0935'},
            {'payload': 2, 'datetime': '20200201T1935'},
            {'payload': 2, 'datetime': '20191211T0935'}
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertTrue(result['status'])

    def test_fail_validate_payload(self):
        """
        Testing wrongly crafted datetime field
        """
        data = [
            {'payload': 'w', 'datetime': '20190201T0935'},
            {'payload': '2.2', 'datetime': '20190201T0935'},
            {'payload': 2.2, 'datetime': '20190201T0935'},
            {'payload': '-2.0', 'datetime': '20190201T0935'},
            {'payload': '2.0', 'datetime': '20190201T0935'},
            {'payload': '-2.0', 'datetime': '20190201T0935'},
            {'payload': 'mame', 'datetime': '20190201T0935'},
            {'payload': '2,0', 'datetime': '20190201T0935'},
            {'payload': '-2,0', 'datetime': '20190201T0935'},
            {'payload': '2:0', 'datetime': '20190201T0935'},
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertFalse(result['status'])

    def test_pass_validate_payload(self):
        """
        Testing well crafted datetime field
        """
        data = [
            {'payload': 2, 'datetime': '20190201T0935'},
            {'payload': -2, 'datetime': '20191211T0935'},
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertTrue(result['status'])

    def test_right_sign_for_failed_datetime_validation(self):
        """
        Testing if the sign for failed datetime validation is correct
        """
        data = {'payload': 2, 'datetime': '129'}
        result = RequestValidator.data_validator(data, schema_names.sensor_data)
        self.assertEqual(result['errors']['datetime'][0], 'Datetime field must be of format %Y%m%dT%H%M')

    def test_expecting_objects_after_validation_1(self):
        """
        Testing if we get the expected object after validation
        """
        data = {'payload': 2, 'datetime': '20190201T0935'}
        expectation = {'payload': 2, 'datetime': '20190201T0935'}
        result = RequestValidator.data_validator(data, schema_names.sensor_data)
        self.assertDictEqual(expectation, result['document'])
