# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentUNB, SyntaxBezeichner, Marktpartner, DatumUhrzeit
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class UNBSegmentConverter(SegmentConverter[SegmentUNB]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentUNB:
        """
        Converts UNB (Interchange Header) segment components to a SegmentUNB object.

        The UNB segment identifies an interchange. It contains the sender and recipient identification, 
        date and time of preparation, and interchange control reference.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentUNB object with syntax identifier, sender, recipient, creation date/time, 
            data exchange reference, application reference, and test indicator

        Example:
        UNB+UNOC:3+4012345678901:14+4012345678901:14+200426:1151+ABC4711++TL++++1'
        """
        syntax_info = MSCONSUtils.split_components(
            string_content=element_components[1]
        )

        absender_info = MSCONSUtils.split_components(
            string_content=element_components[2]
        )

        empfaenger_info = MSCONSUtils.split_components(
            string_content=element_components[3]
        )

        erstellung_info = MSCONSUtils.split_components(
            string_content=element_components[4]
        )

        datenaustauschreferenz = MSCONSUtils.split_components(
            string_content=element_components[5]
        )[0] if len(element_components) > 5 else None

        anwendungsreferenz = MSCONSUtils.split_components(
            string_content=element_components[7]
        )[0] if len(element_components) > 7 else None

        test_kennzeichen = MSCONSUtils.split_components(
            string_content=element_components[11]
        )[0] if len(element_components) > 11 else None

        return SegmentUNB(
            syntax_bezeichner=SyntaxBezeichner(
                syntax_kennung=syntax_info[0],
                syntax_versionsnummer=(syntax_info[1] if len(syntax_info) > 1 else None)
            ),
            absender_der_uebertragungsdatei=Marktpartner(
                marktpartneridentifikationsnummer=absender_info[0],
                teilnehmerbezeichnung_qualifier=absender_info[1]
            ),
            empfaenger_der_uebertragungsdatei=Marktpartner(
                marktpartneridentifikationsnummer=empfaenger_info[0],
                teilnehmerbezeichnung_qualifier=empfaenger_info[1]
            ),
            datum_uhrzeit_der_erstellung=DatumUhrzeit(
                datum=erstellung_info[0],
                uhrzeit=erstellung_info[1]
            ),
            datenaustauschreferenz=datenaustauschreferenz,
            anwendungsreferenz=anwendungsreferenz,
            test_kennzeichen=test_kennzeichen,
        )
