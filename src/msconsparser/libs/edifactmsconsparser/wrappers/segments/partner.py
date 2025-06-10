"""
Models related to partners in the MSCONS message (NAD, CTA, COM in SG2 and SG4).

These models represent market partners and their contact information in the MSCONS message.
According to the MSCONS D.04B 2.4c standard, these segments are used to identify
the sender, receiver, and other parties involved in the message.
"""
from typing import Optional

from pydantic import BaseModel


class IdentifikationDesBeteiligten(BaseModel):
    """
    Identification of the participant (Identifikation des Beteiligten).

    Contains the identification of a market partner and the responsible agency code.

    According to MSCONS D.04B 2.4c, this includes:
    - Party identification (e.g., market partner ID)
    - Code list responsible agency code (e.g., '9' for GS1)
    """
    beteiligter_identifikation: Optional[str] = None  # Marktpartneridentifikationsnummer MP-ID
    verantwortliche_stelle_fuer_die_codepflege_code: Optional[str] = None  # e.g., '9' for GS1


class SegmentNAD(BaseModel):
    """
    NAD-Segment (Name and Address / Name und Adresse)
    M 1 (in SG2)

    Identifies a party by name/address or by a coded identification.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Party qualifier (identifies the role of the party)
    - Party identification (identifies the specific party)

    Common qualifiers include:
    - 'MS': Message sender (Nachrichtenabsender)
    - 'MR': Message recipient (Nachrichtenempfänger)
    - 'DP': Delivery party (Lieferant)
    """
    bezeichner: Optional[str] = None  # technical field
    beteiligter_qualifier: Optional[str] = None  # e.g., 'MS' Nachrichtenabsender, 'MR' Nachrichtenempfänger
    identifikation_des_beteiligten: Optional[IdentifikationDesBeteiligten] = None


class AbteilungOderBearbeiter(BaseModel):
    """
    Department or processor (Abteilung oder Bearbeiter).

    Contains the name of a department or contact person.
    """
    abteilung_oder_bearbeiter: Optional[str] = None  # Name of department or contact person


class SegmentCTA(BaseModel):
    """
    CTA-Segment (Contact Information / Kontaktangabe)

    Identifies a person or department to whom communication should be directed.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Contact function code (identifies the role of the contact)
    - Department or employee (identifies the specific contact)

    Common contact function codes include:
    - 'IC': Information contact (Ansprechpartner)
    """
    funktion_des_ansprechpartners_code: Optional[str] = None  # e.g., 'IC' for Information contact
    abteilung_oder_bearbeiter: Optional[AbteilungOderBearbeiter] = None


class Kommunikationsverbindung(BaseModel):
    """
    Communication connection (Kommunikationsverbindung).

    Contains communication address information such as phone numbers or email addresses.

    According to MSCONS D.04B 2.4c, this includes:
    - Communication address identifier (the actual number or address)
    - Communication address code qualifier (identifies the type of communication)
    """
    kommunikationsadresse_identifikation: Optional[str] = None  # Number, address
    kommunikationsadresse_qualifier: Optional[str] = None  # e.g., 'TE' for telephone, 'EM' for e-mail


class SegmentCOM(BaseModel):
    """
    COM-Segment (Communication Contact / Kommunikationsangabe)

    Identifies the communications number and type of communications used.

    According to MSCONS D.04B 2.4c, this segment includes communication connection information
    such as telephone numbers or email addresses, with qualifiers to identify the type.
    """
    kommunikationsverbindung: Optional[Kommunikationsverbindung] = None


