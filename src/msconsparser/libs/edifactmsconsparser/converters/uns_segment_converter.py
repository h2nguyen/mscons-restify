# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNS
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class UNSSegmentConverter(SegmentConverter[SegmentUNS]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentUNS:
        """
        Converts UNS (Section Control) segment components to a SegmentUNS object.

        The UNS segment is used to separate the header and detail sections of a message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentUNS object with section identification code

        Examples:
        UNS+D'
        """
        abschnittskennung_codiert = element_components[1]
        return SegmentUNS(
            abschnittskennung_codiert=abschnittskennung_codiert
        )
