# coding: utf-8

from abc import ABC, abstractmethod
from typing import Any


class MessageParserPort(ABC):
    """
    Abstract port interface for parsing EDIFACT MSCONS messages.
    
    This port defines the interface for components that can parse EDIFACT MSCONS
    message content and convert it into a structured format.
    
    Attributes:
        None
    """

    @abstractmethod
    def execute(self, edifact_mscons_message_content: str, max_lines_to_parse: int = -1) -> Any:
        """
        Parses an EDIFACT MSCONS message content into a structured format.
        
        Args:
            edifact_mscons_message_content (str): The EDIFACT MSCONS message content to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 which means no parsing limit
            
        Returns:
            Any: The parsed message in a structured format
        """
        pass
