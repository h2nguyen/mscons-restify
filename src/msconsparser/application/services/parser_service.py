# coding: utf-8

from typing import Any

from msconsparser.application.usecases.parse_message_usecase import ParseMessageUseCase


class ParserService:
    """
    Service for parsing EDIFACT MSCONS messages.
    
    This service uses the ParseMessageUseCase to parse EDIFACT MSCONS messages.
    
    Attributes:
        __parse_message_usecase (ParseMessageUseCase): The use case for parsing EDIFACT MSCONS messages
    """

    def __init__(self, parse_message_usecase: ParseMessageUseCase = None) -> None:
        """
        Initializes a new instance of the ParserService class.
        
        Creates a new ParseMessageUseCase instance to use for parsing if one is not provided.
        
        Args:
            parse_message_usecase (ParseMessageUseCase): The use case to use for parsing, defaults to None
        """
        self.__parse_message_usecase = parse_message_usecase or ParseMessageUseCase()

    def parse_message(self, message_content: str, max_lines_to_parse: int = -1) -> Any:
        """
        Parses an EDIFACT MSCONS message content into a structured format.
        
        This method uses the ParseMessageUseCase to parse the message content.
        
        Args:
            message_content (str): The EDIFACT MSCONS message content to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 which means no parsing limit
            
        Returns:
            Any: The parsed message in a structured format (EdifactInterchange)
        """
        return self.__parse_message_usecase.execute(
            edifact_mscons_message_content=message_content,
            max_lines_to_parse=max_lines_to_parse
        )
