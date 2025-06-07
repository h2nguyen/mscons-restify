# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentPIA, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import PIASegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class PIASegmentHandler(SegmentHandler[SegmentPIA]):
    """
    Handler for PIA segments.
    """

    def __init__(self):
        super().__init__(PIASegmentConverter())

    def _update_context(self, segment: SegmentPIA, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted PIA segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted PIA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG9 == current_segment_group:
            context.current_sg9.pia_produktidentifikation = segment