# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentLIN
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class LINSegmentConverter(SegmentConverter[SegmentLIN]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentLIN:
        """
        Converts LIN (Line Item) segment components to a SegmentLIN object.

        The LIN segment identifies a line item and its configuration in a message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentLIN object with position number

        Example:
        LIN+1'
        """
        return SegmentLIN(
            positionsnummer=element_components[1]
        )
