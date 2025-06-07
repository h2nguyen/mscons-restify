# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNT, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import UNTSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class UNTSegmentHandler(SegmentHandler[SegmentUNT]):
    """
    Handler for UNT segments.
    """

    def __init__(self):
        super().__init__(UNTSegmentConverter())

    def _update_context(self, segment: SegmentUNT, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted UNT segment.
        
        Args:
            segment: The converted UNT segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.unt_nachrichtenendsegment = segment