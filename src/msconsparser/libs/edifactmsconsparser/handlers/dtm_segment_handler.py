# coding: utf-8

import logging
from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import DTMSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentDTM

logger = logging.getLogger(__name__)


class DTMSegmentHandler(SegmentHandler[SegmentDTM]):
    """
    Handler for DTM (Date/Time/Period) segments.

    This handler processes DTM segments, which specify dates, times, periods, and their 
    function within the message. It updates the parsing context with the converted DTM 
    segment information, appending it to the appropriate collection based on the current 
    segment group.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the DTM segment handler with the appropriate converter.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(DTMSegmentConverter(syntax_parser=syntax_parser))

    def _update_context(self, segment: SegmentDTM, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted DTM segment.
        The update depends on the current segment group.

        Args:
            segment: The converted DTM segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        if current_segment_group is None:
            context.current_message.dtm_nachrichtendatum.append(segment)
        elif SegmentGroup.SG1 == current_segment_group:
            context.current_sg1.dtm_versionsangabe_marktlokationsscharfe_allokationsliste_gas_mmma.append(segment)
        elif SegmentGroup.SG6 == current_segment_group:
            context.current_sg6.dtm_zeitraeume.append(segment)
        elif SegmentGroup.SG10 == current_segment_group:
            context.current_sg10.dtm_zeitangaben.append(segment)
        else:
            # Unknown segment group
            logger.warning(f"Keine Behandlung für DTM-Segment '{segment}' definiert.")
