# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import NADSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentNAD, SegmentGroup2, SegmentGroup5
)


class NADSegmentHandler(SegmentHandler[SegmentNAD]):
    """
    Handler for NAD (Name and Address) segments.

    This handler processes NAD segments, which identify the market partners and 
    the delivery location. It updates the parsing context with the converted NAD 
    segment information, creating new segment groups (SG2 or SG5) as needed.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the NAD segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(NADSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentNAD, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
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
