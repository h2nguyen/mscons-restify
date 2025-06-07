import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments.location import SegmentLOC
from msconsparser.libs.edifactmsconsparser.converters import LOCSegmentConverter


class TestLOCSegmentConverter(unittest.TestCase):
    """Test case for the LOCSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = LOCSegmentConverter()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["LOC", "237", "11XUENBSOLS----X", "11XVNBSOLS-----X"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentLOC)
        self.assertEqual(result.ortsangabe_qualifier, "237")
        self.assertIsNotNone(result.ortsangabe)
        self.assertEqual(result.ortsangabe.ortsangabe_code, "11XUENBSOLS----X")
        self.assertIsNotNone(result.zugehoeriger_ort_1_identifikation)
        self.assertEqual(result.zugehoeriger_ort_1_identifikation.erster_zugehoeriger_platz_ort_code, "11XVNBSOLS-----X")

    def test_convert_internal_with_only_ortsangabe(self):
        """Test the _convert_internal method with only ortsangabe."""
        # Arrange
        element_components = ["LOC", "107", "11YR000000011247"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentLOC)
        self.assertEqual(result.ortsangabe_qualifier, "107")
        self.assertIsNotNone(result.ortsangabe)
        self.assertEqual(result.ortsangabe.ortsangabe_code, "11YR000000011247")
        self.assertIsNone(result.zugehoeriger_ort_1_identifikation)

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["LOC", "Z04"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentLOC)
        self.assertEqual(result.ortsangabe_qualifier, "Z04")
        self.assertIsNone(result.ortsangabe)
        self.assertIsNone(result.zugehoeriger_ort_1_identifikation)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["LOC"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()
