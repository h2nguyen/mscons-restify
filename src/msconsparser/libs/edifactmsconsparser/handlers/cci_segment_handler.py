# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import CCISegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentCCI, SegmentGroup8
)


class CCISegmentHandler(SegmentHandler[SegmentCCI]):
    """
    Handler for CCI (Characteristic/Class ID) segments.

    This handler processes CCI segments, which specify product characteristics
    and the data that defines those characteristics. It updates the parsing context
    with the converted CCI segment information, creating a new segment group 8 when needed.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the CCI segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(CCISegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentCCI, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted CCI segment.
        The update depends on the current segment group.

        Args:
            segment: The converted CCI segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG8 == current_segment_group:
            context.current_sg8 = SegmentGroup8()
            context.current_sg8.cci_zeitreihentyp = segment
            context.current_sg6.sg8_zeitreihentypen.append(context.current_sg8)
