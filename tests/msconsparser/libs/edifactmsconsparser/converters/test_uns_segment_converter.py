import unittest

from msconsparser.libs.edifactmsconsparser.converters.uns_segment_converter import UNSSegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentUNS


class TestUNSSegmentConverter(unittest.TestCase):
    """Test case for the UNSSegmentConverter class."""

    def setUp(self):
        """Set up the test case."""
        self.context = ParsingContext()
        self.syntax_parser = EdifactSyntaxHelper()
        self.converter = UNSSegmentConverter(syntax_parser=self.syntax_parser)

    def test_convert_internal(self):
        """Test the _convert_internal method."""
        # Arrange
        element_components = ["UNS", "D"]
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
        self.assertIsInstance(result, SegmentUNS)
        self.assertEqual(result.abschnittskennung_codiert, "D")

    def test_convert_with_exception(self):
        """Test the convert method with an exception."""
        # Arrange
        line_number = 1
        element_components = ["UNS"]  # Missing required components
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
