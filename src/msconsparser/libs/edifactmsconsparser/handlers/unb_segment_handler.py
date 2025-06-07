# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNB, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import UNBSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class UNBSegmentHandler(SegmentHandler[SegmentUNB]):
    """
    Handler for UNB segments.
    """

    def __init__(self):
        super().__init__(UNBSegmentConverter())

    def _can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNB segments can always be handled if the interchange exists.
        
        Args:
            context: The parsing context to check.
            
        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNB, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted UNB segment.
        
        Args:
            segment: The converted UNB segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.interchange.unb_nutzdaten_kopfsegment = segment