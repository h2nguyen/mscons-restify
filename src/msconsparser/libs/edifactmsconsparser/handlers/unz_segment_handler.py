# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNZ, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import UNZSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class UNZSegmentHandler(SegmentHandler[SegmentUNZ]):
    """
    Handler for UNZ segments.
    """

    def __init__(self):
        super().__init__(UNZSegmentConverter())

    def _can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNZ segments can be handled if the interchange exists.
        
        Args:
            context: The parsing context to check.
            
        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNZ, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted UNZ segment.
        
        Args:
            segment: The converted UNZ segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.interchange.unz_nutzdaten_endsegment = segment