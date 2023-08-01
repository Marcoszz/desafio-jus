import sys
sys.path.append("utils")

from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.services.process import process_service, ProcessService
from exceptions import ProcessNotFoundException, InvalidCourtException, InvalidSegmentException
from process_validator import ProcessValidator, validator

@patch('src.services.process.selenium_service')
@patch('src.services.process.run')
class TestProcessService(TestCase):
    def test_get_process_only_degree_success(self, run_mock, selenium_service_mock):
        # GIVEN
        stdout_mock = MagicMock()
        stdout_mock.configure_mock(
            **{
                "stdout.strip.return_value": '{"EXAMPLE_KEY": 0}'
            }
        )

        run_mock.return_value = stdout_mock
        selenium_service_mock.get_process_urls.return_value = ['url']
        process = '0710802-55.2018.8.02.0001'

        with patch.object(ProcessService, 'get_court_urls') as get_court_urls_mock:
            get_court_urls_mock.return_value = ['EXAMPLE_VALUE', 'EXAMPLE_VALUE']

            # WHEN
            process_service.get_process(process)

            # THEN
            get_court_urls_mock.assert_called_once_with(process)
            self.assertEqual(len(get_court_urls_mock.return_value), 2)

            selenium_service_mock.get_process_urls.assert_called_once()
            self.assertEqual(len(selenium_service_mock.get_process_urls.return_value), 1)

            run_mock.assert_called_once()

    def test_get_process_full_degree_success(self, run_mock, selenium_service_mock):
        # GIVEN
        stdout_mock = MagicMock()
        stdout_mock.configure_mock(
            **{
                "stdout.strip.return_value": '{"example_key": 0}'
            }
        )

        run_mock.return_value = stdout_mock
        selenium_service_mock.get_process_urls.return_value = ['EXAMPLE_URL', 'EXAMPLE_URL']
        process = '0710802-55.2018.8.02.0001'

        with patch.object(ProcessService, 'get_court_urls') as get_court_urls_mock:
            get_court_urls_mock.return_value = ['EXAMPLE_VALUE', 'EXAMPLE_VALUE']

            # WHEN
            process_service.get_process(process)

            # THEN
            get_court_urls_mock.assert_called_once_with(process)
            self.assertEqual(len(get_court_urls_mock.return_value), 2)

            selenium_service_mock.get_process_urls.assert_called_once()
            self.assertEqual(len(selenium_service_mock.get_process_urls.return_value), 2)

            run_mock.assert_called_once()

    def test_get_process_not_found(self, run_mock, selenium_service_mock):
        # GIVEN
        selenium_service_mock.get_process_urls.return_value = []
        process = '0610802-55.2018.8.02.0001'
        
        with patch.object(ProcessService, 'get_court_urls') as get_court_urls_mock:
            get_court_urls_mock.return_value = ['EXAMPLE_VALUE', 'EXAMPLE_VALUE']
            
            # WHEN / THEN
            with self.assertRaises(ProcessNotFoundException):
                try:
                    process_service.get_process(process)
                except ProcessNotFoundException as e:
                    raise ProcessNotFoundException()
        
            get_court_urls_mock.assert_called_once_with(process)
            self.assertEqual(len(get_court_urls_mock.return_value), 2)

            selenium_service_mock.get_process_urls.assert_called_once()
            self.assertEqual(len(selenium_service_mock.get_process_urls.return_value), 0)

    @patch.object(ProcessValidator, 'region')
    @patch.object(ProcessValidator, 'segment')
    def test_get_process_invalid_segment(self, run_mock, selenium_service_mock, validate_segment_mock, validate_region_mock):
        # GIVEN
        process = '0710802-55.2018.2.02.0001'
        validate_region_mock.return_value = True
        validate_segment_mock.return_value = False
        
        # WHEN / THEN
        with self.assertRaises(InvalidSegmentException):
            try:
                process_service.get_process(process)
            except InvalidSegmentException as e:
                raise InvalidSegmentException()
            
            validate_region_mock.assert_called_once_with(process)
            self.assertTrue(validate_region_mock.return_value)
            validate_segment_mock.assert_called_once_with(process)
            self.assertFalse(validate_segment_mock.return_value)

    @patch.object(ProcessValidator, 'region')
    def test_get_process_invalid_region(self, run_mock, selenium_service_mock, validate_region_mock):
        # GIVEN
        process = '0710802-55.2018.8.05.0001'

        validate_region_mock.return_value = False
          
        # WHEN / THEN
        with self.assertRaises(InvalidCourtException):
            try:
                process_service.get_process(process)
            except InvalidCourtException as e:
                raise InvalidCourtException()
            
            validate_region_mock.assert_called_once_with(process)
            self.assertFalse(validate_region_mock.return_value)

