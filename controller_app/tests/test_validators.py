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
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '129'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201R0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201T2935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '00190201Tw'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20191301T00'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '201999T2935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190101T2935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '2019101T121212'},
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertFalse(result['status'])

    def test_pass_validate_datetime(self):
        """
        Testing well crafted datetime field
        """
        data = [
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20200201T1935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20191211T0935'}
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertTrue(result['status'])

    def test_fail_validate_payload(self):
        """
        Testing wrongly crafted datetime field
        """
        data = [
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 'w', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '2.2', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2.2, 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '-2.0', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '2.0', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '-2.0', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 'mame', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '2,0', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '-2,0', 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': '2:0', 'datetime': '20190201T0935'},
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertFalse(result['status'])

    def test_pass_validate_payload(self):
        """
        Testing well crafted datetime field
        """
        data = [
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201T0935'},
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': -2, 'datetime': '20191211T0935'},
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertTrue(result['status'])

    def test_fail_validation_id(self):
        """
        Tests if the passed by sensor is valid (expecting string)
        """
        data = [
            {'id': 1, 'payload': 2, 'datetime': '20190201T0935'},
            {'id': False, 'payload': 2, 'datetime': '20190201T0935'}
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertFalse(result['status'])

    def test_pass_validation_id(self):
        """
        Tests if an id passed by sensor is valid (expecting string)
        """
        data = [
            {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201T0935'},
            {'id': '1', 'payload': 2, 'datetime': '20190201T0935'}
        ]
        for record in data:
            result = RequestValidator.data_validator(record, schema_names.sensor_data)
            self.assertTrue(result['status'])

    def test_right_sign_for_failed_datetime_validation(self):
        """
        Testing if the sign for failed datetime validation is correct
        """
        data = {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '129'}
        result = RequestValidator.data_validator(data, schema_names.sensor_data)
        self.assertEqual(result['errors']['datetime'][0], 'Datetime field must be of format %Y%m%dT%H%M')

    def test_expecting_objects_after_validation_1(self):
        """
        Testing if we get the expected object after validation
        """
        data = {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201T0935'}
        expectation = {'id': 'a2f182fa-744b-4279-9bad-e35763d68029', 'payload': 2, 'datetime': '20190201T0935'}
        result = RequestValidator.data_validator(data, schema_names.sensor_data)
        self.assertDictEqual(expectation, result['document'])
