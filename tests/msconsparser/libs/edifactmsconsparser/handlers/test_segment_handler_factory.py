import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentType
from msconsparser.libs.edifactmsconsparser.handlers.bgm_segment_handler import BGMSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.cci_segment_handler import CCISegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers import COMSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers import CTASegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.dtm_segment_handler import DTMSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.lin_segment_handler import LINSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.loc_segment_handler import LOCSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.nad_segment_handler import NADSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.pia_segment_handler import PIASegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.qty_segment_handler import QTYSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.rff_segment_handler import RFFSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.segment_handler_factory import SegmentHandlerFactory
from msconsparser.libs.edifactmsconsparser.handlers.sts_segment_handler import STSSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers import UNBSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unh_segment_handler import UNHSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.uns_segment_handler import UNSSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unt_segment_handler import UNTSegmentHandler
from msconsparser.libs.edifactmsconsparser.handlers.unz_segment_handler import UNZSegmentHandler


class TestSegmentHandlerFactory(unittest.TestCase):
    """Test case for the SegmentHandlerFactory class."""

    def setUp(self):
        """Set up the test case."""
        self.factory = SegmentHandlerFactory()

    def test_get_handler_returns_correct_handler_for_each_segment_type(self):
        """Test that get_handler returns the correct handler for each segment type."""
        # Test for each segment type
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNB), UNBSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNH), UNHSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.BGM), BGMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.DTM), DTMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.RFF), RFFSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.NAD), NADSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CTA), CTASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.COM), COMSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNS), UNSSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.LOC), LOCSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.CCI), CCISegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.LIN), LINSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.PIA), PIASegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.QTY), QTYSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.STS), STSSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNT), UNTSegmentHandler)
        self.assertIsInstance(self.factory.get_handler(SegmentType.UNZ), UNZSegmentHandler)

    def test_get_handler_returns_none_for_unknown_segment_type(self):
        """Test that get_handler returns None for an unknown segment type."""
        # Arrange
        unknown_segment_type = "UNKNOWN"

        # Act
        with self.assertLogs(level='WARNING') as cm:
            result = self.factory.get_handler(unknown_segment_type)

        # Assert
        self.assertIsNone(result)
        self.assertIn(f"Kein Handler für Segmenttyp '{unknown_segment_type}' definiert.", cm.output[0])


if __name__ == '__main__':
    unittest.main()