# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNZ
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class UNZSegmentConverter(SegmentConverter[SegmentUNZ]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentUNZ:
        """
        Converts UNZ (Interchange Trailer) segment components to a SegmentUNZ object.

        The UNZ segment is used to end and check the completeness of an interchange.
        It contains the count of messages in the interchange and the interchange reference.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentUNZ object with message count and interchange reference

        Examples:
        UNZ+1+ABC4711'
        """
        anzahl_msg = int(element_components[1])
        datenaustauschreferenz = element_components[2]
        return SegmentUNZ(
            datenaustauschzaehler=anzahl_msg,
            datenaustauschreferenz=datenaustauschreferenz
        )
