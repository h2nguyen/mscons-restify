# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentDTM
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class DTMSegmentConverter(SegmentConverter[SegmentDTM]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentDTM:
        """
        Converts DTM (Date/Time/Period) segment components to a SegmentDTM object.

        The DTM segment specifies dates, times, periods, and their function within the message.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentDTM object with date/time function qualifier, value, and format code

        Examples:
        DTM+137:202106011315?+00:303'
        DTM+157:202002:610'
        DTM+163:202102012300?+00:303'
        DTM+164:202102022300?+00:303'
        DTM+293:20210420103245?+00:304'
        DTM+492:202004:610'
        """
        details = MSCONSUtils.split_components(element_components[1])
        datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier = details[0]
        datum_oder_uhrzeit_oder_zeitspanne_wert = details[1] if len(details) > 1 else None
        datums_oder_uhrzeit_oder_zeitspannen_format_code = details[2] if len(details) > 2 else None

        return SegmentDTM(
            bezeichner=self._get_identifier_name(
                qualifier_code=datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier,
                current_segment_group=current_segment_group
            ),
            datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier=datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier,
            datum_oder_uhrzeit_oder_zeitspanne_wert=datum_oder_uhrzeit_oder_zeitspanne_wert,
            datums_oder_uhrzeit_oder_zeitspannen_format_code=datums_oder_uhrzeit_oder_zeitspannen_format_code
        )

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> Optional[str]:
        if not qualifier_code:
            return None
        elif qualifier_code == "7":
            if current_segment_group == SegmentGroup.SG10:
                return "Nutzungszeitpunkt"
        elif qualifier_code == "9":
            if current_segment_group == SegmentGroup.SG10:
                return "Ablesedatum"
        elif qualifier_code == "60":
            if current_segment_group == SegmentGroup.SG10:
                return "Ausführungs- / Änderungszeitpunkt"
        elif qualifier_code == "137":
            return "Nachrichtendatum"
        elif qualifier_code == "157":
            if current_segment_group == SegmentGroup.SG6:
                return "Gültigkeit, Beginndatum Profilschar"
        elif qualifier_code == "163":
            if current_segment_group == SegmentGroup.SG6:
                return "Beginn Messperiode Übertragungszeitraum"
            elif current_segment_group == SegmentGroup.SG10:
                return "Beginn Messperiode"
        elif qualifier_code == "164":
            if current_segment_group == SegmentGroup.SG6:
                return "Ende Messperiode Übertragungszeitraum"
            elif current_segment_group == SegmentGroup.SG10:
                return "Ende Messperiode"
        elif qualifier_code == "293":
            if current_segment_group == SegmentGroup.SG1:
                return "Versionsangabe marktlokationsscharfe Allokationsliste Gas (MMMA)"
            if current_segment_group == SegmentGroup.SG6:
                return "Versionsangabe"
        elif qualifier_code == "306":
            if current_segment_group == SegmentGroup.SG10:
                return "Leistungsperiode"
        elif qualifier_code == "492":
            if current_segment_group == SegmentGroup.SG6:
                return "Bilanzierungsmonat"
        return None
