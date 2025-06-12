# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentNAD, IdentifikationDesBeteiligten
)


class NADSegmentConverter(SegmentConverter[SegmentNAD]):
    """
    Converter for NAD (Name and Address) segments.

    This converter transforms NAD segment data from EDIFACT format into a structured
    SegmentNAD object. The NAD segment is used to identify the market partners and 
    the delivery location.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the NAD segment converter with the syntax parser.

        Args:
            syntax_parser: The syntax parser to use for parsing segment components.
        """
        super().__init__(syntax_parser=syntax_parser)

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> SegmentNAD:
        """
        Converts NAD (Name and Address) segment components to a SegmentNAD object.

        The NAD segment is used to identify the market partners and the delivery location.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

        Returns:
            SegmentNAD object with function qualifier and either market partner or delivery location

        Examples:
        NAD+MS+9920455302123::293'
        NAD+MR+4012345678901::9'
        NAD+DP'
        """
        beteiligter_qualifier = element_components[1]
        identifikation_des_beteiligten = self._syntax_parser.split_components(element_components[2]) \
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
        """
        Maps NAD qualifier codes to human-readable identifier names.

        This method provides specific mappings for NAD party qualifier codes to meaningful
        names that describe the role of the party in the message.

        Args:
            qualifier_code: The party qualifier code from the NAD segment
            current_segment_group: The current segment group being processed

        Returns:
            A human-readable identifier name for the party role, or None if no mapping exists
        """
        if not qualifier_code:
            return None
        if qualifier_code in ["DP", "DED", "Z15"]:
            return "Name und Adresse"
        if qualifier_code == "MR":
            return "MP-ID Empfänger"
        if qualifier_code == "MS":
            return "MP-ID Absender"
        return None
