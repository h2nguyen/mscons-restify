# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNH, EdifactMSconsMessage, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import UNHSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class UNHSegmentHandler(SegmentHandler[SegmentUNH]):
    """
    Handler for UNH segments.
    """

    def __init__(self):
        super().__init__(UNHSegmentConverter())

    def _can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNH segments can always be handled if the interchange exists.
        
        Args:
            context: The parsing context to check.
            
        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNH, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted UNH segment.
        This also resets the context for a new message.
        
        Args:
            segment: The converted UNH segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        # Reset for a new message
        context.reset_for_new_message()

        # Create a new message and add it to the interchange
        context.current_message = EdifactMSconsMessage(
            unh_nachrichtenkopfsegment=segment
        )
        context.interchange.unh_unt_nachrichten.append(context.current_message)
