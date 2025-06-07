import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentUNB
from msconsparser.libs.edifactmsconsparser.converters import UNBSegmentConverter


class TestUNBSegmentConverter(unittest.TestCase):
    """Test case for the UNBSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = UNBSegmentConverter()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = [
            "UNB", "UNOC:3", "4012345678901:14", "4012345678901:14", 
            "200426:1151", "ABC4711", "", "TL", "", "", "", "1"
        ]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentUNB)
        self.assertEqual(result.syntax_bezeichner.syntax_kennung, "UNOC")
        self.assertEqual(result.syntax_bezeichner.syntax_versionsnummer, "3")
        self.assertEqual(result.absender_der_uebertragungsdatei.marktpartneridentifikationsnummer, "4012345678901")
        self.assertEqual(result.absender_der_uebertragungsdatei.teilnehmerbezeichnung_qualifier, "14")
        self.assertEqual(result.empfaenger_der_uebertragungsdatei.marktpartneridentifikationsnummer, "4012345678901")
        self.assertEqual(result.empfaenger_der_uebertragungsdatei.teilnehmerbezeichnung_qualifier, "14")
        self.assertEqual(result.datum_uhrzeit_der_erstellung.datum, "200426")
        self.assertEqual(result.datum_uhrzeit_der_erstellung.uhrzeit, "1151")
        self.assertEqual(result.datenaustauschreferenz, "ABC4711")
        self.assertEqual(result.anwendungsreferenz, "TL")
        self.assertEqual(result.test_kennzeichen, "1")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = [
            "UNB", "UNOC:3", "4012345678901:14", "4012345678901:14", 
            "200426:1151", "ABC4711"
        ]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentUNB)
        self.assertEqual(result.syntax_bezeichner.syntax_kennung, "UNOC")
        self.assertEqual(result.syntax_bezeichner.syntax_versionsnummer, "3")
        self.assertEqual(result.absender_der_uebertragungsdatei.marktpartneridentifikationsnummer, "4012345678901")
        self.assertEqual(result.absender_der_uebertragungsdatei.teilnehmerbezeichnung_qualifier, "14")
        self.assertEqual(result.empfaenger_der_uebertragungsdatei.marktpartneridentifikationsnummer, "4012345678901")
        self.assertEqual(result.empfaenger_der_uebertragungsdatei.teilnehmerbezeichnung_qualifier, "14")
        self.assertEqual(result.datum_uhrzeit_der_erstellung.datum, "200426")
        self.assertEqual(result.datum_uhrzeit_der_erstellung.uhrzeit, "1151")
        self.assertEqual(result.datenaustauschreferenz, "ABC4711")
        self.assertIsNone(result.anwendungsreferenz)
        self.assertIsNone(result.test_kennzeichen)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["UNB", "UNOC:3"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()