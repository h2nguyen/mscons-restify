import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments.location import SegmentCCI
from msconsparser.libs.edifactmsconsparser.converters.cci_segment_converter import CCISegmentConverter


class TestCCISegmentConverter(unittest.TestCase):
    """Test case for the CCISegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = CCISegmentConverter()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["CCI", "15", "", "BI1"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentCCI)
        self.assertEqual(result.klassentyp_code, "15")
        self.assertIsNotNone(result.merkmalsbeschreibung)
        self.assertEqual(result.merkmalsbeschreibung.merkmal_code, "BI1")

    def test_convert_internal_without_merkmal_code(self):
        """Test the _convert_internal method without merkmal_code."""
        # Arrange
        element_components = ["CCI", "15"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentCCI)
        self.assertEqual(result.klassentyp_code, "15")
        self.assertIsNone(result.merkmalsbeschreibung)

    def test_convert_internal_with_empty_gemessene_dimension_code(self):
        """Test the _convert_internal method with empty gemessene_dimension_code."""
        # Arrange
        element_components = ["CCI", "15", ""]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentCCI)
        self.assertEqual(result.klassentyp_code, "15")
        self.assertIsNone(result.merkmalsbeschreibung)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["CCI"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()
