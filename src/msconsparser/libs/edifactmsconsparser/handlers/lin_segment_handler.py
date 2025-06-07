# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentLIN, SegmentGroup9, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import LINSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class LINSegmentHandler(SegmentHandler[SegmentLIN]):
    """
    Handler for LIN segments.
    """

    def __init__(self):
        super().__init__(LINSegmentConverter())

    def _update_context(self, segment: SegmentLIN, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted LIN segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted LIN segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG9 == current_segment_group:
            context.current_sg9 = SegmentGroup9()
            context.current_sg9.lin_lfd_position = segment
            context.current_sg6.sg9_positionsdaten.append(context.current_sg9)