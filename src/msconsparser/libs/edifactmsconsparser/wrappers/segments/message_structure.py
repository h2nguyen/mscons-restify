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
    bgm_beginn_der_nachricht: Optional[SegmentBGM] = None  # Beginning of message
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
    1. An interchange header (UNB)
    2. One or more MSCONS messages (UNH...UNT)
    3. An interchange trailer (UNZ)

    The interchange serves as an envelope for one or more messages,
    providing information about the sender, receiver, and technical parameters.
    """
    unb_nutzdaten_kopfsegment: Optional[SegmentUNB] = None  # Interchange header
    unh_unt_nachrichten: list[EdifactMSconsMessage] = Field(default_factory=list)  # Messages
    unz_nutzdaten_endsegment: Optional[SegmentUNZ] = None  # Interchange trailer

    def to_json(self) -> str:
        """
        Converts the interchange to a JSON string.

        Returns:
            str: A JSON representation of the interchange with all its messages and segments.
        """
        return json.dumps(self.model_dump(), indent=2, ensure_ascii=False, default=str)
