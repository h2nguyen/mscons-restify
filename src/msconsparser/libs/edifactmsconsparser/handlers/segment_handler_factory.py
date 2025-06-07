# coding: utf-8

import logging
from typing import Dict, Optional

# Keep this style to avoid circular imports
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentType
from msconsparser.libs.edifactmsconsparser.handlers.segment_handler import SegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.bgm_segment_handler import BGMSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.cci_segment_handler import CCISegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.com_segment_handler import COMSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.cta_segment_handler import CTASegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.dtm_segment_handler import DTMSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.lin_segment_handler import LINSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.loc_segment_handler import LOCSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.nad_segment_handler import NADSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.pia_segment_handler import PIASegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.qty_segment_handler import QTYSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.rff_segment_handler import RFFSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.sts_segment_handler import STSSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unb_segment_handler import UNBSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unh_segment_handler import UNHSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.uns_segment_handler import UNSSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unt_segment_handler import UNTSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unz_segment_handler import UNZSegmentHandler

logger = logging.getLogger(__name__)


class SegmentHandlerFactory:
    """
    Factory class for creating segment handlers.
    """

    def __init__(self):
        """
        Initialize the factory with a mapping of segment types to handler classes.
        """
        self.__handlers: Dict[str, SegmentHandler] = {}
        self.__register_handlers()

    def __register_handlers(self) -> None:
        """
        Initialize and register the handlers dictionary with instances of all segment handlers.
        """
        # Initialize handlers for each segment type
        self.__handlers = {
            SegmentType.UNB: UNBSegmentHandler(),
            SegmentType.UNH: UNHSegmentHandler(),
            SegmentType.BGM: BGMSegmentHandler(),
            SegmentType.DTM: DTMSegmentHandler(),
            SegmentType.RFF: RFFSegmentHandler(),
            SegmentType.NAD: NADSegmentHandler(),
            SegmentType.CTA: CTASegmentHandler(),
            SegmentType.COM: COMSegmentHandler(),
            SegmentType.UNS: UNSSegmentHandler(),
            SegmentType.LOC: LOCSegmentHandler(),
            SegmentType.CCI: CCISegmentHandler(),
            SegmentType.LIN: LINSegmentHandler(),
            SegmentType.PIA: PIASegmentHandler(),
            SegmentType.QTY: QTYSegmentHandler(),
            SegmentType.STS: STSSegmentHandler(),
            SegmentType.UNT: UNTSegmentHandler(),
            SegmentType.UNZ: UNZSegmentHandler(),
        }

    def get_handler(self, segment_type: str) -> Optional[SegmentHandler]:
        """
        Get the handler for the specified segment type.

        Args:
            segment_type: The segment type to get a handler for.

        Returns:
            The handler for the segment type, or None if no handler is found.
        """
        handler = self.__handlers.get(segment_type)
        if not handler:
            logger.warning(f"Kein Handler für Segmenttyp '{segment_type}' definiert.")
        return handler
