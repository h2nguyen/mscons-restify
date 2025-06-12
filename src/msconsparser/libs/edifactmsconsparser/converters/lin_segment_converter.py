# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentLIN


class LINSegmentConverter(SegmentConverter[SegmentLIN]):
    """
    Converter for LIN (Line Item) segments.

    This converter transforms LIN segment data from EDIFACT format into a structured
    SegmentLIN object. The LIN segment identifies a line item and its configuration 
    in a message.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the LIN segment converter with the syntax parser.

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
    ) -> SegmentLIN:
        """
        Converts LIN (Line Item) segment components to a SegmentLIN object.

        The LIN segment identifies a line item and its configuration in a message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentLIN object with position number

        Example:
        LIN+1'
        """
        return SegmentLIN(
            positionsnummer=element_components[1]
        )
