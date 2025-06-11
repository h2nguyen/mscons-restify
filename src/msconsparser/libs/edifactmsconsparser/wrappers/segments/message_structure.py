"""
Models for the complete MSCONS message structure.

These models represent the overall structure of MSCONS messages and interchanges.
According to the MSCONS D.04B 2.4c standard, an interchange can contain multiple
messages, and each message follows a specific structure with segment groups.
"""
import json
from typing import Optional

from pydantic import BaseModel, Field

from msconsparser.libs.edifactmsconsparser.wrappers.segments.interchange import SegmentUNB, SegmentUNZ
from msconsparser.libs.edifactmsconsparser.wrappers.segments.message import SegmentUNH, SegmentBGM, SegmentUNT, SegmentUNS
from msconsparser.libs.edifactmsconsparser.wrappers.segments.reference import SegmentDTM
from msconsparser.libs.edifactmsconsparser.wrappers.segments.segment_group import SegmentGroup1, SegmentGroup2, SegmentGroup5

class SegmentUNA(BaseModel):
    """
    Models for the UNA segment (Service String Advice).
    The UNA segment, also known as the Service String Advice, is an optional header
    at the beginning of an EDIFACT message. It defines the special characters used
    as delimiters in the message, allowing the message parser to correctly interpret
    the structure and content. When present, it overrides the default delimiters
    defined by the EDIFACT standard.


    The UNA segment is always exactly 9 characters long and each position has a specific meaning:
    1. Position 1–3: Segment tag "UNA"
    2. Position 4: Component data element separator
    3. Position 5: Data element separator
    4. Position 6: Decimal notation mark
    5. Position 7: Release character (escape)
    6. Position 8: Reserved (usually space)
    7. Position 9: Segment terminator

    Example: UNA:+.? '
    """
    component_separator: str  # Position 4: Component separator (:)
    element_separator: str    # Position 5: Data element separator (+)
    decimal_mark: str         # Position 6: Decimal notation mark (.)
    release_character: str    # Position 7: Release character (?)
    reserved: str             # Position 8: Reserved (usually space)
    segment_terminator: str   # Position 9: Segment terminator (')


class EdifactMSconsMessage(BaseModel):
    """
    Represents an EDIFACT-MSCONS message (UNH...UNT).

    According to MSCONS D.04B 2.4c, a message consists of:
    1. A header section with:
       - UNH: Message header (M 1)
       - BGM: Beginning of message (M 1)
       - DTM: Date/time/period (M 9)
       - SG1: Reference (C 9)
       - SG2: Market partner (C 99)
    2. A section control segment (UNS) separating header and detail
    3. A detail section with:
       - SG5: Delivery/supply location (M 99999)
    4. A message trailer (UNT)

    This structure follows the branching diagram in the MSCONS documentation,
    which shows the hierarchical relationship between segments and segment groups.
    """
    unh_nachrichtenkopfsegment: Optional[SegmentUNH] = None  # Message header
    bgm_beginn_der_nachricht: Optional[SegmentBGM] = None  # Beginning of a message
    dtm_nachrichtendatum: list[SegmentDTM] = Field(default_factory=list)  # Message date
    sg1_referenzen: list[SegmentGroup1] = Field(default_factory=list)  # References
    sg2_marktpartnern: list[SegmentGroup2] = Field(default_factory=list)  # Market partners
    uns_abschnitts_kontrollsegment: Optional[SegmentUNS] = None  # Section control
    sg5_liefer_bzw_bezugsorte: list[SegmentGroup5] = Field(default_factory=list)  # Delivery locations
    unt_nachrichtenendsegment: Optional[SegmentUNT] = None  # Message trailer


class EdifactInterchange(BaseModel):
    """
    Combines all messages, framed by UNB...UNZ (Nutzdaten-Kopfsegment...Nutzdaten-Endesegment).

    According to MSCONS D.04B 2.4c, an interchange consists of:
    1. An optional service string advice (UNA)
    2. An interchange header (UNB)
    3. One or more MSCONS messages (UNH...UNT)
    4. An interchange trailer (UNZ)

    The interchange serves as an envelope for one or more messages,
    providing information about the sender, receiver, and technical parameters.
    The UNA segment, when present, defines the special characters used as delimiters.
    """
    una_service_string_advice: Optional[SegmentUNA] = None  # Service string advice
    unb_nutzdaten_kopfsegment: SegmentUNB = None # Interchange header
    unh_unt_nachrichten: list[EdifactMSconsMessage] = Field(default_factory=list)  # Messages
    unz_nutzdaten_endsegment: SegmentUNZ = None # Interchange trailer

    def to_json(self) -> str:
        """
        Converts the interchange to a JSON string.

        Returns:
            str: A JSON representation of the interchange with all its messages and segments.
        """
        return json.dumps(self.model_dump(), indent=2, ensure_ascii=False, default=str)
