# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentQTY, SegmentGroup10, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import QTYSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class QTYSegmentHandler(SegmentHandler[SegmentQTY]):
    """
    Handler for QTY segments.
    """

    def __init__(self):
        super().__init__(QTYSegmentConverter())

    def _update_context(self, segment: SegmentQTY, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted QTY segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted QTY segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG10 == current_segment_group:
            context.current_sg10 = SegmentGroup10()
            context.current_sg10.qty_mengenangaben = segment
            context.current_sg9.sg10_mengen_und_statusangaben.append(context.current_sg10)