# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import COMSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCOM


class COMSegmentHandler(SegmentHandler[SegmentCOM]):
    """
    Handler for COM (Communication Contact) segments.

    This handler processes COM segments, which provide communication information 
    such as telephone numbers, email addresses, etc. It updates the parsing context
    with the converted COM segment information, appending it to the appropriate segment group.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the COM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(COMSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentCOM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted COM segment.
        The update depends on the current segment group.

        Args:
            segment: The converted COM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG4 == current_segment_group:
            context.current_sg4.com_kommunikationsverbindung.append(segment)
