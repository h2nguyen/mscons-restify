# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCOM, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import COMSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class COMSegmentHandler(SegmentHandler[SegmentCOM]):
    """
    Handler for COM segments.
    """

    def __init__(self):
        super().__init__(COMSegmentConverter())

    def _update_context(self, segment: SegmentCOM, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
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