# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCCI, Merkmalsbeschreibung
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class CCISegmentConverter(SegmentConverter[SegmentCCI]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentCCI:
        """
        Converts CCI (Characteristic/Class ID) segment components to a SegmentCCI object.

        The CCI segment is used to specify product characteristics and the data that defines those characteristics.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentCCI object with class type code and characteristic description

        Example:
        CCI+15++BI1'
        """
        klassentyp_code = element_components[1]
        gemessene_dimension_code = element_components[2] if len(element_components) > 2 and element_components[2] != "" else None
        merkmal_code = element_components[3] if len(element_components) > 3 else None

        return SegmentCCI(
            klassentyp_code=klassentyp_code,
            merkmalsbeschreibung=Merkmalsbeschreibung(
                merkmal_code=merkmal_code
            ) if merkmal_code else None
        )
