"""
Models related to references in the MSCONS message (RFF, DTM in SG1).

These models represent date/time information and references in the MSCONS message.
According to the MSCONS D.04B 2.4c standard, these segments are used to provide
additional reference information and date/time specifications.
"""
from typing import Optional

from pydantic import BaseModel


class SegmentDTM(BaseModel):
    """
    DTM-Segment (Date/Time/Period / Datums-/Zeitangabe)
    M 9 (in SG1) or C 9 depending on the group

    Contains date or time information in code form.

    According to MSCONS D.04B 2.4c, this segment can include:
    - Date/time/period qualifier (e.g., '137' for Document/message date/time)
    - Date/time/period value (the actual date/time value)
    - Date/time/period format code (e.g., '303' for CCYYMMDDHHMMZZZ)

    Common qualifiers include:
    - '137': Document/message date/time (Nachrichtendatum/-zeit)
    - '163': Processing period, start date/time (Verarbeitung, Beginndatum/-zeit)
    - '164': Processing period, end date/time (Verarbeitung, Endedatum/-zeit)
    """
    bezeichner: Optional[str] = None  # technical field
    datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier: Optional[str] = None  # e.g., '137' Dokumenten-/Nachrichtendatum/-zeit
    datum_oder_uhrzeit_oder_zeitspanne_wert: Optional[str] = None  # e.g., '202308150730000'
    datums_oder_uhrzeit_oder_zeitspannen_format_code: Optional[str] = None  # e.g., '303' (Format CCYYMMDDHHMMZZZ)


class SegmentRFF(BaseModel):
    """
    RFF-Segment (Reference / Referenzangabe)
    M 1 (in SG1)

    References another identifier (e.g., order number, process ID).

    According to MSCONS D.04B 2.4c, this segment includes:
    - Reference qualifier (identifies the type of reference)
    - Reference number (the actual reference value)

    Common qualifiers include:
    - 'Z13': Process ID (Prüfidentifikator)
    - 'AGI': Application number (Beantragungsnummer)
    - 'ACW': Previous message (Vorangegangene Nachricht)
    - '23': Device number (Gerätenummer)
    - '24': Configuration ID (Konfigurations-ID)
    """
    bezeichner: Optional[str] = None  # technical field
    referenz_qualifier: Optional[str] = None  # e.g., 'Z13' Prüfidentifikator
    referenz_identifikation: Optional[str] = None  # e.g., '13025'


