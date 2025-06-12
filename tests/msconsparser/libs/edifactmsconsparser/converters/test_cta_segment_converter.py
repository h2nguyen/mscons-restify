import unittest

from msconsparser.libs.edifactmsconsparser.converters import CTASegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments.partner import SegmentCTA


class TestCTASegmentConverter(unittest.TestCase):
    """Test case for the CTASegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = CTASegmentConverter(syntax_parser=self.syntax_parser)
        self.context = ParsingContext()

    def test_convert_internal_with_all_components(self):
        """Test the _convert_internal method with all components."""
        # Arrange
        element_components = ["CTA", "IC", ":P GETTY"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentCTA)
        self.assertEqual(result.funktion_des_ansprechpartners_code, "IC")
        self.assertIsNotNone(result.abteilung_oder_bearbeiter)
        self.assertEqual(result.abteilung_oder_bearbeiter.abteilung_oder_bearbeiter, "P GETTY")

    def test_convert_internal_without_abteilung_oder_bearbeiter(self):
        """Test the _convert_internal method without abteilung_oder_bearbeiter."""
        # Arrange
        element_components = ["CTA", "IC"]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentCTA)
        self.assertEqual(result.funktion_des_ansprechpartners_code, "IC")
        self.assertIsNone(result.abteilung_oder_bearbeiter)

    def test_convert_internal_with_empty_abteilung_oder_bearbeiter(self):
        """Test the _convert_internal method with empty abteilung_oder_bearbeiter."""
        # Arrange
        element_components = ["CTA", "IC", ""]
        last_segment_type = None
        current_segment_group = None

        # Act
        result = self.converter._convert_internal(
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=self.context
        )

        # Assert
        self.assertIsInstance(result, SegmentCTA)
        self.assertEqual(result.funktion_des_ansprechpartners_code, "IC")
        self.assertIsNone(result.abteilung_oder_bearbeiter)

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["CTA"]  # Missing required components
        last_segment_type = None
        current_segment_group = None

        # Act & Assert
        with self.assertRaises(Exception):
            self.converter.convert(
                line_number=line_number,
                element_components=element_components,
                last_segment_type=last_segment_type,
                current_segment_group=current_segment_group,
                context=self.context
            )


if __name__ == '__main__':
    unittest.main()
