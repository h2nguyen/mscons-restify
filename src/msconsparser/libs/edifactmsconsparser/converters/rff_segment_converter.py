# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentRFF
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class RFFSegmentConverter(SegmentConverter[SegmentRFF]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentRFF:
        """
        Converts RFF (Name and Address) segment components to a SegmentRFF object.

        The RFF segment is used to specify the reference information, e.g.: verification identifier,
        configuration ID, the device number or previous master data message of the Metering Point Operator (MSB)

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentRFF object with function qualifier, reference qualifier and identification

        Examples:
        RFF+AGI:AFN9523'
        """
        details = MSCONSUtils.split_components(element_components[1])
        qualifier = details[0]
        identification = details[1]

        return SegmentRFF(
            bezeichner=self._get_identifier_name(
                qualifier_code=qualifier,
                current_segment_group=current_segment_group
            ),
            referenz_qualifier=qualifier,
            referenz_identifikation=identification
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> Optional[str]:
        if not qualifier_code:
            return None
        if qualifier_code in ["ACW", "AGI"]:
            return "Referenzangaben"
        if qualifier_code == "AGK":
            return "Konfigurations-ID"
        if qualifier_code == "MG":
            return "Gerätenummer"
        if qualifier_code == "Z13":
            return "Prüfidentifikator"
        if qualifier_code == "Z30":
            return "Referenz auf vorherige Stammdatenmeldung des MSB"
        return None
