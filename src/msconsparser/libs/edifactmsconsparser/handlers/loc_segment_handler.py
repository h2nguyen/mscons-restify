# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentLOC, SegmentGroup6, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import LOCSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class LOCSegmentHandler(SegmentHandler[SegmentLOC]):
    """
    Handler for LOC segments.
    """

    def __init__(self):
        super().__init__(LOCSegmentConverter())

    def _update_context(self, segment: SegmentLOC, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted LOC segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted LOC segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG6 == current_segment_group:
            if not context.current_sg6:
                context.current_sg6 = SegmentGroup6()
            context.current_sg6.loc_identifikationsangabe = segment
            context.current_sg5.sg6_wert_und_erfassungsangaben_zum_objekt.append(context.current_sg6)