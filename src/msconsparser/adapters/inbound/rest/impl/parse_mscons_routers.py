# coding: utf-8

import logging
import time

from pydantic import StrictStr, Field, StrictBool
from starlette.responses import JSONResponse
from typing_extensions import Annotated

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
    providing an HTTP interface to the parsing functionality.
    """

    def __init__(
        self,
        parser_service: ParserService = None,
    ):
        """
        Initialize the ParseMSCONSRouter with a parser service.

        Args:
            parser_service (ParserService, optional): The parser service to use.
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
            body (str): The raw MSCONS message to parse
            limit_mode (bool): The flag indicating whether to limit the parsed data

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 200)
                or an error message (status 400)
        """
        try:
            parsed_mscons_obj = await self.__get_parsed_result(body, limit_mode)
        except CONTRLException as ex:
            return JSONResponse(status_code=400, content={"error_message": str(ex)})
        except MSCONSParserException as ex:
            return JSONResponse(status_code=400, content={"error_message": str(ex)})
        return JSONResponse(status_code=200, content=parsed_mscons_obj.model_dump())

    async def download_parsed_result(
        self,
        body: Annotated[StrictStr, Field(description="The raw MSCONS message as plain text.")],
    ) -> JSONResponse:
        """
        Parse a raw MSCONS message and return the result as a downloadable JSON file.

        This endpoint accepts a raw MSCONS message string and returns
        the parsed data as a downloadable JSON file.

        Args:
            body (str): The raw MSCONS message to parse

        Returns:
            JSONResponse: A JSON response containing either the parsed data (status 200)
                or an error message (status 400), with headers set for file download
        """
        try:
            parsed_mscons_obj = await self.__get_parsed_result(body, False)
        except CONTRLException as ex:
            return JSONResponse(status_code=400, content={"error_message": str(ex)})
        except MSCONSParserException as ex:
            return JSONResponse(status_code=400, content={"error_message": str(ex)})

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return JSONResponse(
            status_code=200,
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
        logger.info(f"PERFORMANCE: Parsing took {(t2 - t1):2.2f}s")
        return parsed_mscons_obj