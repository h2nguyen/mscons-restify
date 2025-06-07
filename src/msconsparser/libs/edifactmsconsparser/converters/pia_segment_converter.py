# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentPIA, WarenLeistungsnummerIdentifikation
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class PIASegmentConverter(SegmentConverter[SegmentPIA]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentPIA:
        """
        Converts PIA (Product identification) segment components to a SegmentPIA object.

        The PIA segment is used to specify the product identification for the current
        item using the OBIS identifier or the medium.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentPIA object with product identification qualifier, goods/service number
            identification and type of product/service code

        Examples:
        PIA+5+1-1?:1.8.1:SRW'
        PIA+5+1-1?:1.29.1:SRW' - Example of product identification using an OBIS code
        PIA+5+AUA:Z08' - Example of product identification using a medium
        """
        produkt_erzeugnisnummer_qualifier = element_components[1]
        waren_leistungsnummer_identifikation = None
        produkt_leistungsnummer = None
        art_der_produkt_leistungsnummer_code = None

        if len(element_components) > 2:
            # Split the components using the utility method that respects escape sequences
            components = MSCONSUtils.split_components(element_components[2])

            # If there are components (at least one colon that's not escaped)
            if len(components) > 1:
                # The last component is the code, everything before is the product number
                art_der_produkt_leistungsnummer_code = components[-1]
                # Join all components except the last one with colons to form the product number
                produkt_leistungsnummer = MSCONSUtils.COMPONENT_SEPARATOR.join(components[:-1])
                waren_leistungsnummer_identifikation = [produkt_leistungsnummer, art_der_produkt_leistungsnummer_code]
            else:
                # If there are no colons or all colons are escaped, treat the entire string as the product number
                waren_leistungsnummer_identifikation = [element_components[2]]
                produkt_leistungsnummer = element_components[2]
                art_der_produkt_leistungsnummer_code = None

        return SegmentPIA(
            produkt_erzeugnisnummer_qualifier=produkt_erzeugnisnummer_qualifier,
            waren_leistungsnummer_identifikation=WarenLeistungsnummerIdentifikation(
                produkt_leistungsnummer=produkt_leistungsnummer if produkt_leistungsnummer else None,
                art_der_produkt_leistungsnummer_code=art_der_produkt_leistungsnummer_code if art_der_produkt_leistungsnummer_code else None
            ) if waren_leistungsnummer_identifikation else None
        )
