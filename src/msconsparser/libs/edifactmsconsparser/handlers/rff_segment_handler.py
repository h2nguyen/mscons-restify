# coding: utf-8

import logging
from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentRFF, SegmentGroup1, SegmentGroup7, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import RFFSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler

logger = logging.getLogger(__name__)


class RFFSegmentHandler(SegmentHandler[SegmentRFF]):
    """
    Handler for RFF segments.
    """

    def __init__(self):
        super().__init__(RFFSegmentConverter())

    def _update_context(self, segment: SegmentRFF, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted RFF segment.
        The update depends on the current segment group.
        
        Args:
            segment: The converted RFF segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if SegmentGroup.SG1 == current_segment_group:
            context.current_sg1 = SegmentGroup1()
            context.current_sg1.rff_referenzangaben = segment
            context.current_message.sg1_referenzen.append(context.current_sg1)
        elif SegmentGroup.SG7 == current_segment_group:
            context.current_sg7 = SegmentGroup7()
            context.current_sg7.rff_referenzangabe = segment
            context.current_sg6.sg7_referenzangaben.append(context.current_sg7)