# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentCOM, Kommunikationsverbindung
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class COMSegmentConverter(SegmentConverter[SegmentCOM]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentCOM:
        """
        Converts COM (Communication Contact) segment components to a SegmentCOM object.

        The COM segment provides communication information such as telephone numbers, email addresses, etc.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentCOM object with communication connection details

        Examples:
        COM+?+3222271020:TE'
        COM+email@example.com:EM
        """
        kommunikationsverbindung = MSCONSUtils.split_components(string_content=element_components[1])

        return SegmentCOM(
            kommunikationsverbindung=Kommunikationsverbindung(
                kommunikationsadresse_identifikation=kommunikationsverbindung[0],
                kommunikationsadresse_qualifier=kommunikationsverbindung[1] if len(
                    kommunikationsverbindung) > 1 else None
            )
        )
