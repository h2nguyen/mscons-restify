# coding: utf-8

class MSCONSUtils:
    """
    Utility class for handling EDIFACT MSCONS format parsing.

    This class provides constants and methods for parsing EDIFACT MSCONS messages,
    including segment terminators, element separators, component separators, and
    release indicators (escape characters). It also includes methods for splitting
    strings according to EDIFACT syntax rules, respecting escape sequences.

    Attributes:
        SEGMENT_TERMINATOR: Character that marks the end of a segment.
        ELEMENT_SEPARATOR: Character that separates elements within a segment.
        COMPONENT_SEPARATOR: Character that separates components within an element.
        RELEASE_INDICATOR: Escape character used to include special characters in data, e.g. "+" or ":".
    """

    SEGMENT_TERMINATOR = "'"
    ELEMENT_SEPARATOR = "+"
    COMPONENT_SEPARATOR = ":"
    RELEASE_INDICATOR = "?"

    @staticmethod
    def split_segments(string_content: str) -> list[str]:
        """
        Splits a string into segments using the segment terminator.

        Args:
            string_content: The input string to split.

        Returns:
            A list of string segments.
        """
        return string_content.split(MSCONSUtils.SEGMENT_TERMINATOR)

    @staticmethod
    def split_components(string_content: str) -> list[str]:
        """
        Splits a string into components using the component separator,
        respecting escape sequences.

        Args:
            string_content: The input string to split.

        Returns:
            A list of string components with escaped separators preserved.
        """
        return MSCONSUtils.__escape_split(
            string_content=string_content,
            escape_symbol=MSCONSUtils.RELEASE_INDICATOR,
            delimiter=MSCONSUtils.COMPONENT_SEPARATOR
        )

    @staticmethod
    def split_elements(string_content: str) -> list[str]:
        """
        Splits a string into elements using the element separator,
        respecting escape sequences.

        Args:
            string_content: The input string to split.

        Returns:
            A list of string elements with escaped separators preserved.
        """
        return MSCONSUtils.__escape_split(
            string_content=string_content,
            escape_symbol=MSCONSUtils.RELEASE_INDICATOR,
            delimiter=MSCONSUtils.ELEMENT_SEPARATOR
        )

    @staticmethod
    def __escape_split(
            string_content: str,
            escape_symbol: str,
            delimiter: str
    ) -> list[str]:
        """
        Splits a string by the given delimiter while respecting escape sequences.

        Args:
            string_content: The input string to split.
            escape_symbol: The character used to escape the delimiter.
            delimiter: The character to split on.

        Returns:
            A list of string segments with escaped delimiters preserved.
        """
        parts = []
        current = ""
        string_position = 0

        while string_position < len(string_content):
            char = string_content[string_position]

            if char == escape_symbol and string_position + 1 < len(string_content):
                # Escape character found, include next character literally
                current += string_content[string_position + 1]
                string_position += 2
            elif char == delimiter:
                # Delimiter found (not escaped), split here
                parts.append(current)
                current = ""
                string_position += 1
            else:
                current += char
                string_position += 1

        parts.append(current)
        return parts
