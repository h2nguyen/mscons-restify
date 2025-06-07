# coding: utf-8

import logging
from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentDTM, ParsingContext
from msconsparser.libs.edifactmsconsparser.converters import DTMSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler

logger = logging.getLogger(__name__)


class DTMSegmentHandler(SegmentHandler[SegmentDTM]):
    """
    Handler for DTM segments.
    """

    def __init__(self):
        super().__init__(DTMSegmentConverter())

    def _update_context(self, segment: SegmentDTM, current_segment_group: Optional[SegmentGroup], context: ParsingContext) -> None:
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