# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import QTYSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentQTY, SegmentGroup10
)


class QTYSegmentHandler(SegmentHandler[SegmentQTY]):
    """
    Handler for QTY (Quantity) segments.

    This handler processes QTY segments, which specify quantities for the current 
    item position, including the quantity value and unit of measurement. It updates 
    the parsing context with the converted QTY segment information, creating a new 
    segment group 10 when needed.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the QTY segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(QTYSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentQTY, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
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
