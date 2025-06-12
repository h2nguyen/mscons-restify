# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import UNTSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNT


class UNTSegmentHandler(SegmentHandler[SegmentUNT]):
    """
    Handler for UNT (Message Trailer) segments.

    This handler processes UNT segments, which are used to end and check the completeness 
    of a message. It updates the parsing context with the converted UNT segment information, 
    which includes the count of segments in the message and the message reference number.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNT segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(UNTSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentUNT, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNT segment.

        Args:
            segment: The converted UNT segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.unt_nachrichtenendsegment = segment
