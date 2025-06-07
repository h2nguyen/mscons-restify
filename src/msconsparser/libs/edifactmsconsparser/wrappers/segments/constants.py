"""
Constants and enumerations for the MSCONS message structure.
"""
import sys
from enum import Enum

# --- Fallback implementation for StrEnum for Python < 3.11 ---
if sys.version_info >= (3, 11):
    pass
else:
    class StrEnum(str, Enum):
        """
        Simple emulation of StrEnum for Python versions
        before 3.11 (values behave like strings).
        """
        pass


class SegmentGroup(StrEnum):
    """
    Segment groups in the MSCONS message structure.
    """
    SG1 = "SG1"
    SG2 = "SG2"
    SG3 = "SG3"
    SG4 = "SG4"
    SG5 = "SG5"
    SG6 = "SG6"
    SG7 = "SG7"
    SG8 = "SG8"
    SG9 = "SG9"
    SG10 = "SG10"


class SegmentType(StrEnum):
    """
    EDIFACT segment identifiers (MSCONS D.04B 2.4c).
    The German names are based on the official MSCONS message description,
    see https://bdew-mako.de/pdf/MSCONS_MIG_2_4c_20231024.pdf
    """
    UNA = "UNA"  # Service String Advice: Defines the EDIFACT separators.
    UNB = "UNB"  # Interchange Header - Encloses the data exchange.
    UNZ = "UNZ"  # Interchange Trailer - Closing record of the interchange.
    UNH = "UNH"  # Message Header - Beginning of an MSCONS message.
    UNT = "UNT"  # Message Trailer - End of an MSCONS message.
    BGM = "BGM"  # Beginning of Message - Message type/reference.
    DTM = "DTM"  # Date/Time/Period, e.g., 137=Message time, 163/164=Interval start/end.
    RFF = "RFF"  # Reference, e.g., Z13=Process ID, 23=Device number, 24=Configuration ID.
    NAD = "NAD"  # Name and Address - Partner identification (MS/MR/DP) or delivery location.
    CTA = "CTA"  # Contact Information - Contact person (Qualifier IC).
    COM = "COM"  # Communication Contact, e.g., TE=Telephone, EM=E-mail.
    LOC = "LOC"  # Place/Location Identification - Balance group (16) or object (17).
    UNS = "UNS"  # Section Control - Separates header and detail section.
    LIN = "LIN"  # Line Item - Sequential position within the position group.
    PIA = "PIA"  # Additional Product ID - Additional product/device ID.
    QTY = "QTY"  # Quantity, e.g., 220 = Measured value of the tariff period.
    CCI = "CCI"  # Marking of the time series type (Composite Code Information).
    MOA = "MOA"  # Monetary Amount - Monetary values in the header.
    FTX = "FTX"  # Free Text - Comments, explanatory texts.
    STS = "STS"  # Status - Plausibility, substitute value method, correction reason, gas quality, etc.

    # Add more segments according to MSCONS-MIG as needed...