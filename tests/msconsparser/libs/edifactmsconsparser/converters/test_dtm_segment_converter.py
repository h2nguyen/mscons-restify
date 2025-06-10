import unittest

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup
from msconsparser.libs.edifactmsconsparser.wrappers.segments.reference import SegmentDTM
from msconsparser.libs.edifactmsconsparser.converters.dtm_segment_converter import DTMSegmentConverter


class TestDTMSegmentConverter(unittest.TestCase):
    """Test case for the DTMSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.converter = DTMSegmentConverter()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["DTM", "137:202106011315+00:303"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Nachrichtendatum")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202106011315+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_internal_with_segment_group(self):
        """Test the _convert_internal method with a specific segment group."""
        # Arrange
        element_components = ["DTM", "163:202102012300+00:303"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG6

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Beginn Messperiode Übertragungszeitraum")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "163")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202102012300+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_internal_with_different_segment_group(self):
        """Test the _convert_internal method with a different segment group."""
        # Arrange
        element_components = ["DTM", "163:202102012300+00:303"]
        last_segment_type = None
        current_segment_group = SegmentGroup.SG10

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Beginn Messperiode")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "163")
        self.assertEqual(result.datum_oder_uhrzeit_oder_zeitspanne_wert, "202102012300+00")
        self.assertEqual(result.datums_oder_uhrzeit_oder_zeitspannen_format_code, "303")

    def test_convert_internal_with_minimal_components(self):
        """Test the _convert_internal method with minimal components."""
        # Arrange
        element_components = ["DTM", "137"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(element_components, last_segment_type, current_segment_group)

        # Assert
        self.assertIsInstance(result, SegmentDTM)
        self.assertEqual(result.bezeichner, "Nachrichtendatum")
        self.assertEqual(result.datums_oder_uhrzeits_oder_zeitspannen_funktion_qualifier, "137")
        self.assertIsNone(result.datum_oder_uhrzeit_oder_zeitspanne_wert)
        self.assertIsNone(result.datums_oder_uhrzeit_oder_zeitspannen_format_code)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["DTM"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(line_number, element_components, last_segment_type, current_segment_group)


if __name__ == '__main__':
    unittest.main()
