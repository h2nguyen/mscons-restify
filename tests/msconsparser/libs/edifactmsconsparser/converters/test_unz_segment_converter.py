import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentUNZ
from msconsparser.libs.edifactmsconsparser.converters import UNZSegmentConverter


class TestUNZSegmentConverter(unittest.TestCase):
    """Test case for the UNZSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = UNZSegmentConverter()

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["UNZ", "1", "ABC4711"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentUNZ)
        self.assertEqual(result.datenaustauschzaehler, 1)
        self.assertEqual(result.datenaustauschreferenz, "ABC4711")

    def test_convert_with_exception_missing_components(self):
        """Test the convert method with an exception due to missing components."""
        # Arrange
        line_number = 1
        element_components = ["UNZ", "1"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)

    def test_convert_with_invalid_datenaustauschzaehler(self):
        """Test the convert method with an exception due to invalid datenaustauschzaehler."""
        # Arrange
        line_number = 1
        element_components = ["UNZ", "invalid", "ABC4711"]  # Invalid datenaustauschzaehler
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()