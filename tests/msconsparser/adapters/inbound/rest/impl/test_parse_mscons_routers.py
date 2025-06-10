import unittest
from unittest.mock import patch, MagicMock

import pytest
from fastapi import status
from starlette.responses import JSONResponse

from msconsparser.adapters.inbound.rest.impl.parse_mscons_routers import ParseMSCONSRouter
from msconsparser.libs.edifactmsconsparser.exceptions import CONTRLException, MSCONSParserException


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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_parse_mscons_raw_format_mscons_parser_exception(self):
        """Test that parse_mscons_raw_format handles MSCONSParserException correctly."""
        # Setup
        error_message = "MSCONS parser error message"
        self.mock_parser_service.parse_message.side_effect = MSCONSParserException(error_message)
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_raw_format(limit_mode, "invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    @patch('time.perf_counter')
    async def test_parse_mscons_file_success(self, mock_perf_counter):
        """Test that parse_mscons_file returns parsed data on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_file = "test_mscons_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_file(limit_mode, mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=mscons_file, max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    async def test_parse_mscons_file_no_file(self):
        """Test that parse_mscons_file handles no file provided correctly."""
        # Setup
        mscons_file = None
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_file(limit_mode, mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), '{"error_message":"No file provided"}')

    @pytest.mark.asyncio
    async def test_parse_mscons_file_contrl_exception(self):
        """Test that parse_mscons_file handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)
        mscons_file = "invalid_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_file(limit_mode, mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_parse_mscons_file_mscons_parser_exception(self):
        """Test that parse_mscons_file handles MSCONSParserException correctly."""
        # Setup
        error_message = "MSCONS parser error message"
        self.mock_parser_service.parse_message.side_effect = MSCONSParserException(error_message)
        mscons_file = "invalid_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_file(limit_mode, mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_parse_mscons_file_bytes(self):
        """Test that parse_mscons_file handles bytes content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_file = b"test_mscons_data"
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_file(limit_mode, mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_mscons_data", max_lines_to_parse=-1)

    @pytest.mark.asyncio
    async def test_parse_mscons_file_tuple(self):
        """Test that parse_mscons_file handles tuple content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_file = ("filename.txt", b"test_mscons_data")
        limit_mode = False

        # Execute
        response = await self.router.parse_mscons_file(limit_mode, mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_mscons_data", max_lines_to_parse=-1)

    @pytest.mark.asyncio
    @patch('time.strftime')
    @patch('time.perf_counter')
    async def test_download_parsed_result_success(self, mock_perf_counter, mock_strftime):
        """Test that download_parsed_result returns downloadable JSON on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_strftime.return_value = "20230101_120000"
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_input = "test_mscons_data"

        # Execute
        response = await self.router.download_parsed_result(mscons_input)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=mscons_parsed_20230101_120000.json")
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=mscons_input, max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    async def test_download_parsed_result_contrl_exception(self):
        """Test that download_parsed_result handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)

        # Execute
        response = await self.router.download_parsed_result("invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_download_parsed_result_mscons_parser_exception(self):
        """Test that download_parsed_result handles MSCONSParserException correctly."""
        # Setup
        error_message = "MSCONS parser error message"
        self.mock_parser_service.parse_message.side_effect = MSCONSParserException(error_message)

        # Execute
        response = await self.router.download_parsed_result("invalid_data")

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    @patch('time.strftime')
    @patch('time.perf_counter')
    async def test_download_parsed_file_result_success(self, mock_perf_counter, mock_strftime):
        """Test that download_parsed_file_result returns downloadable JSON on success."""
        # Setup
        mock_perf_counter.side_effect = [1.0, 2.0]  # t1=1.0, t2=2.0
        mock_strftime.return_value = "20230101_120000"
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_file = "test_mscons_data"

        # Execute
        response = await self.router.download_parsed_file_result(mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.assertEqual(response.headers["Content-Disposition"], "attachment; filename=mscons_parsed_20230101_120000.json")
        self.mock_parser_service.parse_message.assert_called_once_with(message_content=mscons_file, max_lines_to_parse=-1)
        mock_parsed_obj.model_dump.assert_called_once()

    @pytest.mark.asyncio
    async def test_download_parsed_file_result_no_file(self):
        """Test that download_parsed_file_result handles no file provided correctly."""
        # Setup
        mscons_file = None

        # Execute
        response = await self.router.download_parsed_file_result(mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), '{"error_message":"No file provided"}')

    @pytest.mark.asyncio
    async def test_download_parsed_file_result_contrl_exception(self):
        """Test that download_parsed_file_result handles CONTRLException correctly."""
        # Setup
        error_message = "CONTRL error message"
        self.mock_parser_service.parse_message.side_effect = CONTRLException(error_message)
        mscons_file = "invalid_data"

        # Execute
        response = await self.router.download_parsed_file_result(mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_download_parsed_file_result_mscons_parser_exception(self):
        """Test that download_parsed_file_result handles MSCONSParserException correctly."""
        # Setup
        error_message = "MSCONS parser error message"
        self.mock_parser_service.parse_message.side_effect = MSCONSParserException(error_message)
        mscons_file = "invalid_data"

        # Execute
        response = await self.router.download_parsed_file_result(mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.body.decode(), f'{{"error_message":"{error_message}"}}')

    @pytest.mark.asyncio
    async def test_download_parsed_file_result_bytes(self):
        """Test that download_parsed_file_result handles bytes content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_file = b"test_mscons_data"

        # Execute
        response = await self.router.download_parsed_file_result(mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_mscons_data", max_lines_to_parse=-1)

    @pytest.mark.asyncio
    async def test_download_parsed_file_result_tuple(self):
        """Test that download_parsed_file_result handles tuple content correctly."""
        # Setup
        mock_parsed_obj = MagicMock()
        mock_parsed_obj.model_dump.return_value = {"key": "value"}
        self.mock_parser_service.parse_message.return_value = mock_parsed_obj
        mscons_file = ("filename.txt", b"test_mscons_data")

        # Execute
        response = await self.router.download_parsed_file_result(mscons_file)

        # Verify
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.body.decode(), '{"key":"value"}')
        self.mock_parser_service.parse_message.assert_called_once_with(message_content="test_mscons_data", max_lines_to_parse=-1)


if __name__ == "__main__":
    unittest.main()
