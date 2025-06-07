# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentBGM, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import BGMSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class BGMSegmentHandler(SegmentHandler[SegmentBGM]):
    """
    Handler for BGM segments.
    """

    def __init__(self):
        super().__init__(BGMSegmentConverter())

    def _update_context(self, segment: SegmentBGM, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
        """
        Update the context with the converted BGM segment.

        Args:
            segment: The converted BGM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        context.current_message.bgm_beginn_der_nachricht = segment
