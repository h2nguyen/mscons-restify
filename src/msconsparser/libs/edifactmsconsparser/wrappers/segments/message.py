"""
Models related to the EDIFACT message structure (UNH, UNT, BGM, UNS).

These models represent the structure of an MSCONS message within an interchange.
According to the MSCONS D.04B 2.4c standard, each message starts with UNH, 
contains a BGM and other segments, and ends with UNT.
"""
from typing import Optional

from pydantic import BaseModel


class NachrichtenKennung(BaseModel):
    """
    Message identification (Nachrichten-Kennung).

    According to MSCONS D.04B 2.4c, this includes:
    - Message type identifier (e.g., 'MSCONS')
    - Message type version number (e.g., 'D')
    - Message type release number (e.g., '04B')
    - Controlling agency (e.g., 'UN')
    - Association assigned code (e.g., '2.4c')
    """
    nachrichtentyp_kennung: Optional[
        str] = None  # e.g., 'MSCONS' - Bericht über den Verbrauch messbarer Dienstleistungen
    versionsnummer_des_nachrichtentyps: Optional[str] = None  # e.g., 'D' - Entwurfs-Version
    freigabenummer_des_nachrichtentyps: Optional[str] = None  # e.g., '04B' - Ausgabe 2004-B
    verwaltende_organisation: Optional[str] = None  # e.g., 'UN' - UN/CEFACT
    anwendungscode_der_zustaendigen_organisation: Optional[
        str] = None  # e.g., '2.4c' - Versionsnummer der zugrundeliegenden BDEW-Nachrichtenbeschreibung


class StatusDerUebermittlung(BaseModel):
    """
    Transmission status (Status der Übermittlung).

    Used for message series splitting when a message is too large.
    Contains:
    - Transmission sequence number
    - First/last transmission indicator
    """
    uebermittlungsfolgenummer: Optional[str] = None  # Lfd. Nummer in der Serie bei Aufteilung
    erste_und_letzte_uebermittlung: Optional[str] = None  # 'C' für Erste, 'F' für Letzte


class SegmentUNH(BaseModel):
    """
    UNH-Segment (Message Header / Nachrichtenkopfsegment)

    Starts an MSCONS message and contains message identification information.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Message reference number (must match UNT DE0062)
    - Message type identification (MSCONS, version, etc.)
    - Common access reference (only used with S010)
    - Transmission status (for message series splitting)
    """
    nachrichten_referenznummer: Optional[str] = None  # Eindeutige Nachrichtenreferenz des Absenders
    nachrichten_kennung: Optional[NachrichtenKennung] = None
    allgemeine_zuordnungsreferenz: Optional[str] = None  # Nur wenn Datenelementgruppe S010 verwendet wird
    status_der_uebermittlung: Optional[StatusDerUebermittlung] = None


class DokumentenNachrichtenname(BaseModel):
    """
    Document/message name (Dokumenten-/Nachrichtenname).

    Contains the document name code that identifies the type of document.
    According to MSCONS D.04B 2.4c, this can be:
    - '7' for Process data report
    - '270' for Delivery note
    - 'Z48' for Load profile market location, tranche
    - Many other values depending on the specific use case
    """
    dokumentenname_code: Optional[str] = None  # e.g., '7' Prozessdatenbericht, '270' Lieferschein


class DokumentenNachrichtenIdentifikation(BaseModel):
    """
    Document/message identification (Dokumenten-/Nachrichten-Identifikation).

    Contains the unique document number assigned by the sender.
    """
    dokumentennummer: Optional[str] = None  # Eindeutige EDI-Nachrichtennummer, vom Sender vergeben


class SegmentBGM(BaseModel):
    """
    BGM-Segment (Beginning of Message / Beginn der Nachricht)

    Identifies the document type, number, and function.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Document name code (e.g., '7' for Process data report)
    - Document number (unique EDI message number)
    - Message function code (e.g., '9' for Original, '1' for Cancellation)
    """
    dokumenten_nachrichtenname: Optional[DokumentenNachrichtenname] = None
    dokumenten_nachrichten_identifikation: Optional[DokumentenNachrichtenIdentifikation] = None
    nachrichtenfunktion_code: Optional[str] = None  # e.g., '9' Original, '1' Storno


class SegmentUNT(BaseModel):
    """
    UNT-Segment (Message Trailer / Nachrichten-Endesegment)

    Ends an MSCONS message and contains control information.

    According to MSCONS D.04B 2.4c, this segment includes:
    - Number of segments in the message (total count)
    - Message reference number (must match UNH DE0062)
    """
    anzahl_der_segmente_in_einer_nachricht: Optional[int] = None  # Gesamtanzahl Segmente
    nachrichten_referenznummer: Optional[str] = None  # Muss gleich zu UNH DE0062 sein


class SegmentUNS(BaseModel):
    """
    UNS-Segment - Section control segment (Abschnitts-Kontrollsegment)

    Separates the header and detail sections of the message.

    According to MSCONS D.04B 2.4c, this segment typically contains:
    - Section identification code, usually 'D' to separate the header and position parts
    """
    abschnittskennung_codiert: Optional[str] = None  # i.d.R. 'D' für Trennung von Kopf- und Positionsteil
