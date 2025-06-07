import unittest
from unittest.mock import patch, MagicMock

from fastapi import status
from starlette.responses import JSONResponse

from msconsparser.adapters.inbound.rest.impl.parse_mscons_routers import ParseMSCONSRouter
from msconsparser.libs.edifactmsconsparser.exceptions import CONTRLException


class TestParseMSCONSRouter(unittest.TestCase):
    """Test cases for the ParseMSCONSRouter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_parser_service = MagicMock()
        self.router = ParseMSCONSRouter(parser_service=self.mock_parser_service)

    def test_init_with_parser(self):
        """Test that the router can be initialized with a parser service."""
        self.assertEqual(self.router._ParseMSCONSRouter__parser_service, self.mock_parser_service)

    @patch('msconsparser.adapters.inbound.rest.impl.parse_mscons_routers.ParserService')
    def test_init_without_parser(self, mock_parser_service_class):
        """Test that the router creates a new parser service if none is provided."""
        mock_parser_service_instance = MagicMock()
        mock_parser_service_class.return_value = mock_parser_service_instance

        router = ParseMSCONSRouter()

        self.assertEqual(router._ParseMSCONSRouter__parser_service, mock_parser_service_instance)
        mock_parser_service_class.assert_called_once()

    @patch('time.perf_counter')
    async def test_parse_mscons_raw_format_success(self, mock_perf_counter):
        """Test that parse_mscons_raw_format returns parsed data on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_input = "test_mscons_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_raw_format(limit_mode, mscons_input)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=mscons_input, max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @patch('time.perf_counter')
    @patch('msconsparser.adapters.inbound.rest.impl.parse_mscons_routers.logger')
    async def test_parse_mscons_raw_format_logs_performance(self, mock_logger, mock_perf_counter):
        """Test that parse_mscons_raw_format logs performance metrics."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 3.5]  # t1=1.0, t2=3.5 (2.5s difference)
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        limit_mode = False

        # Execute
        await self.router.parse_mscons_raw_format(limit_mode, "test_data")

        # Verify
        mock_logger.info.assert_called_once_with("PERFORMANCE: Parsing took 2.50s")

    async def test_parse_mscons_raw_format_contrl_exception(self):
        """Test that parse_mscons_raw_format handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_raw_format(limit_mode, "invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')


if __name__ == "__main__":
    unittest.main()
