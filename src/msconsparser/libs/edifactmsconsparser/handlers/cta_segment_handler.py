# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import CTASegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentCTA, SegmentGroup4
)


class CTASegmentHandler(SegmentHandler[SegmentCTA]):
    """
    Handler for CTA (Contact Information) segments.

    This handler processes CTA segments, which identify a person or department to whom 
    communication should be directed. It updates the parsing context with the converted 
    CTA segment information, creating a new segment group 4 when needed.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the CTA segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(CTASegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentCTA, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted CTA segment.
        The update depends on the current segment group.

        Args:
            segment: The converted CTA segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG4 == current_segment_group:
            context.current_sg4 = SegmentGroup4()
            context.current_sg4.cta_ansprechpartner = segment
            context.current_sg2.sg4_kontaktinformationen.append(context.current_sg4)
