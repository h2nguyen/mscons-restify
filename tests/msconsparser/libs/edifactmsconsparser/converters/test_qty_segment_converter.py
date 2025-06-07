import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments.measurement import SegmentQTY
from msconsparser.libs.edifactmsconsparser.converters import QTYSegmentConverter


class TestQTYSegmentConverter(unittest.TestCase):
    """Test case for the QTYSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = QTYSegmentConverter()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["QTY", "220:4250.465:D54"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4250.465)
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_without_masseinheit_code(self):
        """Test the _convert_internal method without masseinheit_code."""
        # Arrange
        element_components = ["QTY", "67:4250.465"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "67")
        self.assertEqual(result.menge, 4250.465)
        self.assertIsNone(result.masseinheit_code)

    def test_convert_internal_with_decimal_places(self):
        """Test the _convert_internal method with decimal places."""
        # Arrange
        element_components = ["QTY", "220:4.123:D54"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "220")
        self.assertEqual(result.menge, 4.123)
        self.assertEqual(result.masseinheit_code, "D54")

    def test_convert_internal_with_negative_value(self):
        """Test the _convert_internal method with negative value."""
        # Arrange
        element_components = ["QTY", "79:-4.987:KWH"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentQTY)
        self.assertEqual(result.menge_qualifier, "79")
        self.assertEqual(result.menge, -4.987)
        self.assertEqual(result.masseinheit_code, "KWH")

    def test_convert_with_exception_missing_components(self):
        """Test the convert method with an exception due to missing components."""
        # Arrange
        line_number = 1
        element_components = ["QTY"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)

    def test_convert_with_exception_invalid_menge(self):
        """Test the convert method with an exception due to invalid menge."""
        # Arrange
        line_number = 1
        element_components = ["QTY", "220:invalid:D54"]  # Invalid menge
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()
