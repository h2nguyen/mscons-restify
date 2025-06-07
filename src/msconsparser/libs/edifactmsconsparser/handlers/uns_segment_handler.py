# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNS, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import UNSSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class UNSSegmentHandler(SegmentHandler[SegmentUNS]):
    """
    Handler for UNS segments.
    """

    def __init__(self):
        super().__init__(UNSSegmentConverter())

    def _update_context(self, segment: SegmentUNS, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted UNS segment.
        
        Args:
            segment: The converted UNS segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.uns_abschnitts_kontrollsegment = segment