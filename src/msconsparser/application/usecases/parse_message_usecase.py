# coding: utf-8

from typing import Any

from msconsparser.domain.ports.inbound import MessageParserPort
from msconsparser.libs.edifactmsconsparser.edifact_mscons_parser import EdifactMSCONSParser


class ParseMessageUseCase(MessageParserPort):
    """
    Use case implementation for parsing EDIFACT MSCONS messages.
    
    This class implements the MessageParserPort interface and uses the
    EdifactMSCONSParser to perform the actual parsing of EDIFACT MSCONS messages.
    
    Attributes:
        parser (EdifactMSCONSParser): The parser used to parse EDIFACT MSCONS messages
    """

    def __init__(self, parser: EdifactMSCONSParser = None) -> None:
        """
        Initializes a new instance of the ParseMessageUseCase class.
        
        Creates a new EdifactMSCONSParser instance to use for parsing.

        Args:
            parser (EdifactMSCONSParser): The EDIFACT MSCONS parser to use, defaults to None,
        """
        self.__parser = parser or EdifactMSCONSParser()

    def execute(self, edifact_mscons_message_content: str, max_lines_to_parse: int = -1) -> Any:
        """
        Parses an EDIFACT MSCONS message content into a structured format.
        
        Args:
            edifact_mscons_message_content (str): The EDIFACT MSCONS message content to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 which means no parsing limit
            
        Returns:
            Any: The parsed message in a structured format (EdifactInterchange)
        """
        return self.__parser.parse(
            edifact_text=edifact_mscons_message_content,
            max_lines_to_parse=max_lines_to_parse
        )
