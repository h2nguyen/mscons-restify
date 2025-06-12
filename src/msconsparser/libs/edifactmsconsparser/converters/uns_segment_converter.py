# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNS


class UNSSegmentConverter(SegmentConverter[SegmentUNS]):
    """
    Converter for UNS (Section Control) segments.

    This converter transforms UNS segment data from EDIFACT format into a structured
    SegmentUNS object. The UNS segment is used to separate the header and detail 
    sections of a message.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNS segment converter with the syntax parser.

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
    ) -> SegmentUNS:
        """
        Converts UNS (Section Control) segment components to a SegmentUNS object.

        The UNS segment is used to separate the header and detail sections of a message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentUNS object with section identification code

        Examples:
        UNS+D'
        """
        abschnittskennung_codiert = element_components[1]
        return SegmentUNS(
            abschnittskennung_codiert=abschnittskennung_codiert
        )
