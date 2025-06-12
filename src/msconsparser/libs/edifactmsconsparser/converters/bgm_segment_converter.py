# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentBGM, DokumentenNachrichtenname, DokumentenNachrichtenIdentifikation
)


class BGMSegmentConverter(SegmentConverter[SegmentBGM]):
    """
    Converter for BGM (Beginning of Message) segments.

    This converter transforms BGM segment data from EDIFACT format into a structured
    SegmentBGM object. The BGM segment identifies the type and function of a message
    and transmits its identifying number.
    """

    def __init__(self, syntax_parser: EdifactSyntaxHelper):
        """
        Initialize the BGM segment converter with the syntax parser.

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
    ) -> SegmentBGM:
        """
        Converts BGM (beginning of Message) segment components to a SegmentBGM object.

        The BGM segment identifies the type and function of a message and transmits its identifying number.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed
            context: The context to use for the converter.

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
