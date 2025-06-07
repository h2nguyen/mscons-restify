# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentNAD, SegmentGroup2, SegmentGroup5, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import NADSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class NADSegmentHandler(SegmentHandler[SegmentNAD]):
    """
    Handler for NAD segments.
    """

    def __init__(self):
        super().__init__(NADSegmentConverter())

    def _update_context(self, segment: SegmentNAD, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted NAD segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted NAD segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG2 == current_segment_group:
            context.current_sg2 = SegmentGroup2()
            context.current_sg2.nad_marktpartner = segment
            context.current_message.sg2_marktpartnern.append(context.current_sg2)
        elif SegmentGroup.SG5 == current_segment_group:
            if not context.current_sg5:
                context.current_sg5 = SegmentGroup5()
            context.current_sg5.nad_name_und_adresse = segment
            context.current_message.sg5_liefer_bzw_bezugsorte.append(context.current_sg5)