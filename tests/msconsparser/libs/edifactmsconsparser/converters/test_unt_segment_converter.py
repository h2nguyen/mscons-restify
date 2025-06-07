import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentUNT
from msconsparser.libs.edifactmsconsparser.converters import UNTSegmentConverter


class TestUNTSegmentConverter(unittest.TestCase):
    """Test case for the UNTSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = UNTSegmentConverter()

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["UNT", "39", "1"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentUNT)
        self.assertEqual(result.anzahl_der_segmente_in_einer_nachricht, 39)
        self.assertEqual(result.nachrichten_referenznummer, "1")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "39"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)

    def test_convert_with_invalid_segment_count(self):
        """Test the convert method with invalid segment count."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "invalid", "1"]  # Invalid segment count
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()