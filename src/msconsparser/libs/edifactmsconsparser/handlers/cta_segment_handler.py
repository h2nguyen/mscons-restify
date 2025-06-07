# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCTA, SegmentGroup4, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import CTASegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class CTASegmentHandler(SegmentHandler[SegmentCTA]):
    """
    Handler for CTA segments.
    """

    def __init__(self):
        super().__init__(CTASegmentConverter())

    def _update_context(self, segment: SegmentCTA, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
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