# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentNAD, IdentifikationDesBeteiligten
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class NADSegmentConverter(SegmentConverter[SegmentNAD]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentNAD:
        """
        Converts NAD (Name and Address) segment components to a SegmentNAD object.

        The NAD segment is used to identify the market partners and the delivery location.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentNAD object with function qualifier and either market partner or delivery location

        Examples:
        NAD+MS+9920455302123::293'
        NAD+MR+4012345678901::9'
        NAD+DP'
        """
        beteiligter_qualifier = element_components[1]
        identifikation_des_beteiligten = MSCONSUtils.split_components(element_components[2]) \
            if len(element_components) > 2 else None

        return SegmentNAD(
            bezeichner=self._get_identifier_name(
                qualifier_code=beteiligter_qualifier,
                current_segment_group=current_segment_group
            ),
            beteiligter_qualifier=beteiligter_qualifier,
            identifikation_des_beteiligten=IdentifikationDesBeteiligten(
                beteiligter_identifikation=identifikation_des_beteiligten[0],
                verantwortliche_stelle_fuer_die_codepflege_code=identifikation_des_beteiligten[2]
            ) if identifikation_des_beteiligten and len(identifikation_des_beteiligten) > 2 else None
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> Optional[str]:
        if not qualifier_code:
            return None
        if qualifier_code in ["DP", "DED", "Z15"]:
            return "Name und Adresse"
        if qualifier_code == "MR":
            return "MP-ID Empfänger"
        if qualifier_code == "MS":
            return "MP-ID Absender"
        return None
