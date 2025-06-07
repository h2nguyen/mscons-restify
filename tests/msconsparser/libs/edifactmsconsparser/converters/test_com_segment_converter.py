import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments.partner import SegmentCOM
from msconsparser.libs.edifactmsconsparser.converters import COMSegmentConverter


class TestCOMSegmentConverter(unittest.TestCase):
    """Test case for the COMSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = COMSegmentConverter()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["COM", "3222271020:TE"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentCOM)
        self.assertIsNotNone(result.kommunikationsverbindung)
        self.assertEqual(result.kommunikationsverbindung.kommunikationsadresse_identifikation, "3222271020")
        self.assertEqual(result.kommunikationsverbindung.kommunikationsadresse_qualifier, "TE")

    def test_convert_internal_without_qualifier(self):
        """Test the _convert_internal method without qualifier."""
        # Arrange
        element_components = ["COM", "email@example.com"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentCOM)
        self.assertIsNotNone(result.kommunikationsverbindung)
        self.assertEqual(result.kommunikationsverbindung.kommunikationsadresse_identifikation, "email@example.com")
        self.assertIsNone(result.kommunikationsverbindung.kommunikationsadresse_qualifier)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["COM"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()
