"""
Models related to the EDIFACT interchange structure (UNB, UNZ).

These models represent the interchange envelope that contains one or more MSCONS messages.
According to the MSCONS D.04B 2.4c standard, the interchange is framed by UNB (header) and UNZ (trailer) segments.
"""
from typing import Optional

from pydantic import BaseModel


class SyntaxBezeichner(BaseModel):
    """
    Syntax identifier and version (Syntax-Kennung).

    Contains the EDIFACT syntax identifier (e.g., 'UNOC' for UN/ECE character set C)
    and the syntax version number (e.g., '3' for Version 3).
    """
    syntax_kennung: Optional[str] = None  # e.g., 'UNOC' for UN/ECE character set C
    syntax_versionsnummer: Optional[str] = None  # e.g., '3' for Version 3


class Marktpartner(BaseModel):
    """
    Market partner identification (Marktpartner).

    Contains the market partner identification number (MP-ID) and
    the qualifier for the participant designation (e.g., '14' for GS1).
    """
    marktpartneridentifikationsnummer: Optional[str] = None  # MP-ID of sender/receiver
    teilnehmerbezeichnung_qualifier: Optional[str] = None  # e.g., '14' for GS1, '500'/'502' for DE


class DatumUhrzeit(BaseModel):
    """
    Date and time of creation (Datum/Uhrzeit der Erstellung).

    Contains the date in format YYMMDD and time in format HHMM.
    """
    datum: Optional[str] = None  # Format: YYMMDD
    uhrzeit: Optional[str] = None  # Format: HHMM


class SegmentUNB(BaseModel):
    """
    UNB-Segment (Interchange Header / Nutzdaten-Kopfsegment)

    Contains information about sender/receiver address, date/time, etc.
    This is the first segment of an EDIFACT interchange and defines the
    communication partners and technical parameters.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Syntax identifier and version
    - Sender identification
    - Receiver identification
    - Date and time of creation
    - Interchange reference
    - Application reference (e.g., 'EM' for energy quantity, 'TL' for load profile)
    - Test indicator
    """
    syntax_bezeichner: Optional[SyntaxBezeichner] = None
    absender_der_uebertragungsdatei: Optional[Marktpartner] = None
    empfaenger_der_uebertragungsdatei: Optional[Marktpartner] = None
    datum_uhrzeit_der_erstellung: Optional[DatumUhrzeit] = None
    datenaustauschreferenz: Optional[str] = None  # Unique reference to identify the file
    anwendungsreferenz: Optional[str] = None  # e.g., 'EM' for energy quantity, 'TL' for load profile
    test_kennzeichen: Optional[str] = None  # '1' if test transmission


class SegmentUNZ(BaseModel):
    """
    UNZ-Segment (Interchange Trailer / Nutzdaten-Endesegment)

    Closes the interchange and contains control information.
    This is the last segment of an EDIFACT interchange.

    According to MSCONS D.04B 2.4c, this segment includes:
    - The total number of messages in the interchange
    - The interchange reference (must match the reference in UNB)
    """
    datenaustauschzaehler: Optional[int] = None  # Total number of messages in the interchange
    datenaustauschreferenz: Optional[str] = None  # Must match DE0020 in the UNB segment
