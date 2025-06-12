# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import UNSSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNS


class UNSSegmentHandler(SegmentHandler[SegmentUNS]):
    """
    Handler for UNS (Section Control) segments.

    This handler processes UNS segments, which are used to separate the header and 
    detail sections of a message. It updates the parsing context with the converted 
    UNS segment information.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNS segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(UNSSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentUNS, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNS segment.

        Args:
            segment: The converted UNS segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.uns_abschnitts_kontrollsegment = segment
