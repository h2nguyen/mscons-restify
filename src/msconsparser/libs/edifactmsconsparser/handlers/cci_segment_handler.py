# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCCI, SegmentGroup8, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import CCISegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class CCISegmentHandler(SegmentHandler[SegmentCCI]):
    """
    Handler for CCI segments.
    """

    def __init__(self):
        super().__init__(CCISegmentConverter())

    def _update_context(self, segment: SegmentCCI, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
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