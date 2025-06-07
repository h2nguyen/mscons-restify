# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCTA, AbteilungOderBearbeiter
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class CTASegmentConverter(SegmentConverter[SegmentCTA]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentCTA:
        """
        Converts CTA (Contact Information) segment components to a SegmentCTA object.

        The CTA segment identifies a person or department to whom communication should be directed.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentCTA object with contact function code and department or employee information

        Example:
        CTA+IC+:P GETTY'
        """
        funktion_des_ansprechpartners_code = element_components[1]
        abteilung_oder_bearbeiter = MSCONSUtils.split_components(element_components[2]) \
            if len(element_components) > 2 else None

        return SegmentCTA(
            funktion_des_ansprechpartners_code=funktion_des_ansprechpartners_code,
            abteilung_oder_bearbeiter=AbteilungOderBearbeiter(
                abteilung_oder_bearbeiter=abteilung_oder_bearbeiter[1]
            ) if abteilung_oder_bearbeiter is not None and len(abteilung_oder_bearbeiter) > 1 else None
        )
