import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments.measurement import SegmentLIN
from msconsparser.libs.edifactmsconsparser.converters import LINSegmentConverter


class TestLINSegmentConverter(unittest.TestCase):
    """Test case for the LINSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = LINSegmentConverter()

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["LIN", "1"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentLIN)
        self.assertEqual(result.positionsnummer, "1")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["LIN"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()
