# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentSTS, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import STSSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class STSSegmentHandler(SegmentHandler[SegmentSTS]):
    """
    Handler for STS segments.
    """

    def __init__(self):
        super().__init__(STSSegmentConverter())

    def _update_context(self, segment: SegmentSTS, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted STS segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted STS segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG10 == current_segment_group:
            context.current_sg10.sts_statusangaben.append(segment)