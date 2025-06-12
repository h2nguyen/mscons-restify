# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import UNZSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNZ


class UNZSegmentHandler(SegmentHandler[SegmentUNZ]):
    """
    Handler for UNZ (Interchange Trailer) segments.

    This handler processes UNZ segments, which are used to end and check the completeness 
    of an interchange. It updates the parsing context with the converted UNZ segment 
    information, which includes the count of messages in the interchange and the 
    interchange reference.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the UNZ segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(UNZSegmentConverter(syntax_parser=syntax_parser))

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

    def _update_context(self, segment: SegmentUNZ, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted UNZ segment.

        Args:
            segment: The converted UNZ segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.interchange.unz_nutzdaten_endsegment = segment
