# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNA, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import UNASegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils.mscons_utils import MSCONSUtils


class UNASegmentHandler(SegmentHandler[SegmentUNA]):
    """
    Handler for UNA segments (Service String Advice).
    
    The UNA segment defines the special characters used as delimiters in the EDIFACT message.
    When present, it overrides the default delimiters defined by the EDIFACT standard.
    """

    def __init__(self):
        super().__init__(UNASegmentConverter())

    def _can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.
        UNA segments can always be handled if the interchange exists.
        
        Args:
            context: The parsing context to check.
            
        Returns:
            True if the context is valid, False otherwise.
        """
        return context.interchange is not None

    def _update_context(self, segment: SegmentUNA, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted UNA segment and update the MSCONSUtils delimiters.
        
        Args:
            segment: The converted UNA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        # Store the UNA segment in the interchange
        context.interchange.una_service_string_advice = segment
        
        # Update the MSCONSUtils delimiters
        MSCONSUtils.COMPONENT_SEPARATOR = segment.component_separator
        MSCONSUtils.ELEMENT_SEPARATOR = segment.element_separator
        MSCONSUtils.DECIMAL_MARK = segment.decimal_mark
        MSCONSUtils.RELEASE_INDICATOR = segment.release_character
        MSCONSUtils.RESERVED_INDICATOR = segment.reserved
        MSCONSUtils.SEGMENT_TERMINATOR = segment.segment_terminator
