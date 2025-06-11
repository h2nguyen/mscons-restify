# coding: utf-8

import logging
import time
from typing import Union, Tuple
from typing_extensions import Annotated

from fastapi import status
from pydantic import StrictStr, Field, StrictBool, StrictBytes
from starlette.responses import JSONResponse

from msconsparser.adapters.inbound.rest.apis.mscons_parser_api_base import BaseMSCONSParserApi
from msconsparser.libs.edifactmsconsparser.exceptions import CONTRLException, MSCONSParserException
from msconsparser.application.services import ParserService

logger = logging.getLogger(__name__)

MAX_LINES_TO_PARSE = 2442
UNLIMITED_LINES_TO_PARSE_INDICATOR = -1

class ParseMSCONSRouter(BaseMSCONSParserApi):
    """
    Router class for handling MSCONS message parsing requests.

    This class implements the API for parsing EDIFACT MSCONS messages,
    providing an HTTP interface to the parsing functionality. It supports
    parsing raw MSCONS messages as text or from uploaded files, with options
    to limit the number of lines parsed and to download the results as JSON files.
    """

    def __init__(
        self,
        parser_service: ParserService = None,
    ):
        """
        Initialize the ParseMSCONSRouter with a parser service.

        Args:
            parser_service (ParserService): The parser service to use.
                If None, a new ParserService instance will be created.
        """
        self.__parser_service = parser_service or ParserService()

    async def parse_mscons_raw_format(
        self,
        limit_mode: Annotated[StrictBool, Field(description="If true, enables the parsing limit for max number of lines, as per default it is maximum 2442 lines.")],
        body: Annotated[StrictStr, Field(description="The raw MSCONS message as plain text.")],
    ) -> JSONResponse:
        """
        Parse a raw MSCONS message and return the result as JSON.

        This endpoint accepts a raw MSCONS message string and returns
        the parsed data in a structured JSON format.

        Args:
            limit_mode (bool): If true, limits parsing to a maximum of 2442 lines;
                if false, parses the entire message regardless of size
            body (str): The raw MSCONS message to parse

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 200 - Success)
                or an error message (status 400 - Bad request)
        """
        try:
            parsed_mscons_obj = await self.__get_parsed_result(body, limit_mode)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except MSCONSParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_mscons_obj.model_dump())

    async def parse_mscons_file(
        self,
        limit_mode: Annotated[StrictBool, Field(description="If true, enables the parsing limit for max number of lines, as per default it is maximum 2442 lines.")],
        body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The raw MSCONS message as a file.")],
    ) -> JSONResponse:
        """
        Parse a raw MSCONS message from a file and return the result as JSON.

        This endpoint accepts an uploaded file containing a raw MSCONS message
        and returns the parsed data in a structured JSON format. The method handles
        different file content formats and converts bytes to strings, attempting UTF-8
        decoding first and falling back to ISO-8859-1 if UTF-8 decoding fails.

        Args:
            limit_mode (bool): If true, limits parsing to a maximum of 2442 lines;
                if false, parses the entire message regardless of size
            body (str | dict[str, bytes]): The uploaded file containing the raw MSCONS message,
                which may be a tuple or direct file content in various formats

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 200 - Success)
                or an error message (status 400 - Bad request)
        """
        if not body:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": "No file provided"})

        file_content = await self.__get_file_content(body)

        try:
            parsed_mscons_obj = await self.__get_parsed_result(file_content, limit_mode)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except MSCONSParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        return JSONResponse(status_code=status.HTTP_200_OK, content=parsed_mscons_obj.model_dump())

    async def download_parsed_result(
        self,
        body: Annotated[StrictStr, Field(description="The raw MSCONS message as plain text.")],
    ) -> JSONResponse:
        """
        Parse a raw MSCONS message and return the result as a downloadable JSON file.

        This endpoint accepts a raw MSCONS message string and returns
        the parsed data as a downloadable JSON file. Unlike parse_mscons_raw_format,
        this method always parses the entire message without line limits and sets
        appropriate headers for file download.

        Args:
            body (str): The raw MSCONS message to parse

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 201 - Created)
                or an error message (status 400 - Bad request), with headers set for file download
                including a timestamp in the filename
        """
        try:
            parsed_mscons_obj = await self.__get_parsed_result(body, False)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except MSCONSParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=parsed_mscons_obj.model_dump(),
            headers={"Content-Disposition": f"attachment; filename=mscons_parsed_{timestamp}.json"}
        )

    async def download_parsed_file_result(
        self,
        body: Annotated[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]], Field(description="The raw MSCONS message as a file.")],
    ) -> JSONResponse:
        """
        Parse a raw MSCONS message from a file and return the result as a downloadable JSON file.

        This endpoint accepts an uploaded file containing a raw MSCONS message
        and returns the parsed data as a downloadable JSON file. The method handles
        different file content formats, converts bytes to strings (attempting UTF-8
        decoding first and falling back to ISO-8859-1 if UTF-8 decoding fails),
        and always parses the entire message without line limits.

        Args:
            body (str | dict[str, bytes]): The uploaded file containing the raw MSCONS message,
                which may be a tuple or direct file content in various formats

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 201 - Created)
                or an error message (status 400 - Bad request), with headers set for file download
                including a timestamp in the filename
        """
        if not body:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": "No file provided"})

        file_content = await self.__get_file_content(body)

        try:
            parsed_mscons_obj = await self.__get_parsed_result(file_content, False)
        except CONTRLException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except MSCONSParserException as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})
        except Exception as ex:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error_message": str(ex)})

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=parsed_mscons_obj.model_dump(),
            headers={"Content-Disposition": f"attachment; filename=mscons_parsed_{timestamp}.json"}
        )

    async def __get_parsed_result(self, body, limit_mode):
        max_lines_to_parse = MAX_LINES_TO_PARSE if limit_mode else UNLIMITED_LINES_TO_PARSE_INDICATOR
        t1 = time.perf_counter()
        parsed_mscons_obj = self.__parser_service.parse_message(
            message_content=body,
            max_lines_to_parse=max_lines_to_parse
        )
        t2 = time.perf_counter()
        logger.info(f"SPEED-TEST: Parsing took {(t2 - t1):2.2f}s")
        return parsed_mscons_obj

    @staticmethod
    async def __get_file_content(body):
        file_content = body
        if isinstance(file_content, bytes):
            try:
                file_content = file_content.decode('utf-8')
            except UnicodeDecodeError:
                # Fall back to ISO-8859-1 (Latin-1) which is a common encoding for EDIFACT files
                # and can handle all byte values from 0x00 to 0xFF
                file_content = file_content.decode('iso-8859-1')
        return file_content
