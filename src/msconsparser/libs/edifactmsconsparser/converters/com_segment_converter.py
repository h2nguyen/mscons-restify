# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentCOM, Kommunikationsverbindung
)


class COMSegmentConverter(SegmentConverter[SegmentCOM]):
    """
    Converter for COM (Communication Contact) segments.

    This converter transforms COM segment data from EDIFACT format into a structured
    SegmentCOM object. The COM segment provides communication information such as 
    telephone numbers, email addresses, etc.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the COM segment converter with the syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser=syntax_parser)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentCOM:
        """
        Converts COM (Communication Contact) segment components to a SegmentCOM object.

        The COM segment provides communication information such as telephone numbers, email addresses, etc.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentCOM object with communication connection details

        Examples:
        COM+?+3222271020:TE'
        COM+email@example.com:EM
        """
        kommunikationsverbindung = self._syntax_parser.split_components(string_content=element_components[1])

        return SegmentCOM(
            kommunikationsverbindung=Kommunikationsverbindung(
                kommunikationsadresse_identifikation=kommunikationsverbindung[0],
                kommunikationsadresse_qualifier=kommunikationsverbindung[1] if len(
                    kommunikationsverbindung) > 1 else None
            )
        )
