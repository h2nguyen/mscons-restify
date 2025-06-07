# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentBGM, \
    DokumentenNachrichtenname, DokumentenNachrichtenIdentifikation
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class BGMSegmentConverter(SegmentConverter[SegmentBGM]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentBGM:
        """
        Converts BGM (Beginning of Message) segment components to a SegmentBGM object.

        The BGM segment identifies the type and function of a message and transmits its identifying number.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentBGM object with document name, document identification, and message function code

        Example:
        BGM+7+MSI5422+9'
        """
        dokumentenname_code = element_components[1]
        dokumentennummer = element_components[2]
        nachrichtenfunktion_code = element_components[3] if len(element_components) > 3 else None

        return SegmentBGM(
            dokumenten_nachrichtenname=DokumentenNachrichtenname(
                dokumentenname_code=dokumentenname_code
            ),
            dokumenten_nachrichten_identifikation=DokumentenNachrichtenIdentifikation(
                dokumentennummer=dokumentennummer
            ),
            nachrichtenfunktion_code=nachrichtenfunktion_code
        )
