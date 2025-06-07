# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNT
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class UNTSegmentConverter(SegmentConverter[SegmentUNT]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentUNT:
        """
        Converts UNT (Message Trailer) segment components to a SegmentUNT object.

        The UNT segment is used to end and check the completeness of a message.
        It contains the count of segments in the message and the message reference number.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentUNT object with segment count and message reference number

        Examples:
        UNT+39+1'
        """
        anzahl_der_segmente_in_einer_nachricht = int(element_components[1])
        nachrichten_referenznummer = element_components[2]

        return SegmentUNT(
            anzahl_der_segmente_in_einer_nachricht=anzahl_der_segmente_in_einer_nachricht,
            nachrichten_referenznummer=nachrichten_referenznummer
        )
