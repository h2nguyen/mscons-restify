import unittest

from msconsparser.libs.edifactmsconsparser.utils.edifact_syntax_helper import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.exceptions.parser_exceptions import MSCONSParserException
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import EdifactInterchange, SegmentUNA
from msconsparser.libs.edifactmsconsparser.wrappers.segments.constants import EdifactConstants, SegmentType


class TestEdifactSyntaxHelper(unittest.TestCase):
    """Test case for the EdifactSyntaxHelper class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = EdifactSyntaxHelper()
        self.context = ParsingContext()
        self.context.interchange = EdifactInterchange()
        self.context.interchange.una_service_string_advice = SegmentUNA(
            component_separator=";",
            element_separator="*",
            decimal_mark=",",
            release_character="?",
            reserved=" ",
            segment_terminator="'"
        )

    def test_get_component_separator(self):
        """Test get_component_separator method."""
        # Test with valid context
        self.assertEqual(";", self.parser.get_component_separator(self.context))

        # Test with None context
        self.assertEqual(EdifactConstants.DEFAULT_COMPONENT_SEPARATOR, self.parser.get_component_separator(None))

        # Test with context but None interchange
        context = ParsingContext()
        context.interchange = None
        self.assertEqual(EdifactConstants.DEFAULT_COMPONENT_SEPARATOR, self.parser.get_component_separator(context))

        # Test with context but None una_service_string_advice
        context = ParsingContext()
        context.interchange = EdifactInterchange()
        context.interchange.una_service_string_advice = None
        self.assertEqual(EdifactConstants.DEFAULT_COMPONENT_SEPARATOR, self.parser.get_component_separator(context))

    def test_get_element_separator(self):
        """Test get_element_separator method."""
        # Test with valid context
        self.assertEqual("*", self.parser.get_element_separator(self.context))

        # Test with None context
        self.assertEqual(EdifactConstants.DEFAULT_ELEMENT_SEPARATOR, self.parser.get_element_separator(None))

    def test_get_decimal_mark(self):
        """Test get_decimal_mark method."""
        # Test with valid context
        self.assertEqual(",", self.parser.get_decimal_mark(self.context))

        # Test with None context
        self.assertEqual(EdifactConstants.DEFAULT_DECIMAL_MARK, self.parser.get_decimal_mark(None))

    def test_get_release_indicator(self):
        """Test get_release_indicator method."""
        # Test with valid context
        self.assertEqual("?", self.parser.get_release_indicator(self.context))

        # Test with None context
        self.assertEqual(EdifactConstants.DEFAULT_RELEASE_INDICATOR, self.parser.get_release_indicator(None))

    def test_get_reserved_indicator(self):
        """Test get_reserved_indicator method."""
        # Test with valid context
        self.assertEqual(" ", self.parser.get_reserved_indicator(self.context))

        # Test with None context
        self.assertEqual(EdifactConstants.DEFAULT_RESERVED_INDICATOR, self.parser.get_reserved_indicator(None))

    def test_get_segment_terminator(self):
        """Test get_segment_terminator method."""
        # Test with valid context
        self.assertEqual("'", self.parser.get_segment_terminator(self.context))

        # Test with None context
        self.assertEqual(EdifactConstants.DEFAULT_SEGMENT_TERMINATOR, self.parser.get_segment_terminator(None))

    def test_split_segments(self):
        """Test split_segments method with context."""
        # Test with valid context
        test_data = "UNB*UNOC;3*SENDER;ZZ*RECIPIENT;ZZ*230101;1200*12345'UNH*12345*MSCONS;D;96A;UN;EAN005'"
        result = self.parser.split_segments(test_data, self.context)
        self.assertEqual(3, len(result))  # Including empty string at the end
        self.assertEqual("UNB*UNOC;3*SENDER;ZZ*RECIPIENT;ZZ*230101;1200*12345", result[0])
        self.assertEqual("UNH*12345*MSCONS;D;96A;UN;EAN005", result[1])
        self.assertEqual("", result[2])

        # Test with None context
        test_data = "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345'UNH+12345+MSCONS:D:96A:UN:EAN005'"
        result = self.parser.split_segments(test_data, None)
        self.assertEqual(3, len(result))  # Including empty string at the end
        self.assertEqual("UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345", result[0])
        self.assertEqual("UNH+12345+MSCONS:D:96A:UN:EAN005", result[1])
        self.assertEqual("", result[2])

    def test_split_elements(self):
        """Test split_elements method with context."""
        # Test with valid context
        test_data = "UNB*UNOC;3*SENDER;ZZ*RECIPIENT;ZZ*230101;1200*12345"
        expected = ["UNB", "UNOC;3", "SENDER;ZZ", "RECIPIENT;ZZ", "230101;1200", "12345"]
        self.assertEqual(expected, self.parser.split_elements(test_data, self.context))

        # Test with None context
        test_data = "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345"
        expected = ["UNB", "UNOC:3", "SENDER:ZZ", "RECIPIENT:ZZ", "230101:1200", "12345"]
        self.assertEqual(expected, self.parser.split_elements(test_data, None))

    def test_split_components(self):
        """Test split_components method with context."""
        # Test with valid context
        test_data = "UNOC;3"
        expected = ["UNOC", "3"]
        self.assertEqual(expected, self.parser.split_components(test_data, self.context))

        # Test with None context
        test_data = "UNOC:3"
        expected = ["UNOC", "3"]
        self.assertEqual(expected, self.parser.split_components(test_data, None))

    def test_escape_split(self):
        """Test __escape_split method through split_elements."""
        # Test with escaped delimiters
        test_data = "UNB+UNOC:3+SENDER?+ZZ+RECIPIENT:ZZ+230101:1200+12345"
        expected = ["UNB", "UNOC:3", "SENDER+ZZ", "RECIPIENT:ZZ", "230101:1200", "12345"]
        self.assertEqual(expected, self.parser.split_elements(test_data, None))

        # Test with context and escaped delimiters
        test_data = "UNB*UNOC;3*SENDER?*ZZ*RECIPIENT;ZZ*230101;1200*12345"
        expected = ["UNB", "UNOC;3", "SENDER*ZZ", "RECIPIENT;ZZ", "230101;1200", "12345"]
        self.assertEqual(expected, self.parser.split_elements(test_data, self.context))

    def setUp_segment_types(self):
        """Set up segment types for testing."""
        return [segment_type.value for segment_type in SegmentType]

    def test_remove_invalid_prefix_original_technical_prefix(self):
        """Test remove_invalid_prefix_from_segment_data with the original technical prefix."""
        segment_types = self.setUp_segment_types()

        test_data = "[${test(TEST_DATA)}]:UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        expected = "UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, segment_types, self.context))

    def test_remove_invalid_prefix_none_segment_types(self):
        """Test remove_invalid_prefix_from_segment_data with None segment_types."""
        test_data = "[${test(TEST_DATA)}]:UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        with self.assertRaises(MSCONSParserException) as context:
            self.parser.remove_invalid_prefix_from_segment_data(test_data, None, self.context)
        self.assertTrue("Segment types must not be None nor empty" in str(context.exception))

    def test_remove_invalid_prefix_empty_segment_types(self):
        """Test remove_invalid_prefix_from_segment_data with None segment_types."""
        test_data = "[${test(TEST_DATA)}]:UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        with self.assertRaises(MSCONSParserException) as context:
            self.parser.remove_invalid_prefix_from_segment_data(test_data, [], self.context)
        self.assertTrue("Segment types must not be None nor empty" in str(context.exception))

    def test_remove_invalid_prefix_arbitrary_prefix(self):
        """Test remove_invalid_prefix_from_segment_data with a different arbitrary prefix."""
        segment_types = self.setUp_segment_types()

        test_data = "SOME_RANDOM_PREFIX:UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        expected = "UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, segment_types, self.context))

    def test_remove_invalid_prefix_different_segment_type(self):
        """Test remove_invalid_prefix_from_segment_data with a prefix before a different segment type."""
        segment_types = self.setUp_segment_types()

        test_data = "ANOTHER_PREFIX:UNH+12345+MSCONS:D:96A:UN:EAN005'"
        expected = "UNH+12345+MSCONS:D:96A:UN:EAN005'"
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, segment_types, self.context))

    def test_remove_invalid_prefix_no_prefix(self):
        """Test remove_invalid_prefix_from_segment_data without any prefix."""
        segment_types = self.setUp_segment_types()

        test_data = "UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        expected = "UNB+UNOC:3+9911845000009:500+9901000000001:500+250602:2158+9QF2J8QT6RJCAO++EM'"
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, segment_types, self.context))

    def test_remove_invalid_prefix_empty_string(self):
        """Test remove_invalid_prefix_from_segment_data with an empty string."""
        segment_types = self.setUp_segment_types()

        test_data = ""
        expected = ""
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, segment_types, self.context))

    def test_remove_invalid_prefix_no_segment_type(self):
        """Test remove_invalid_prefix_from_segment_data with a string that doesn't contain any valid segment type."""
        segment_types = self.setUp_segment_types()

        test_data = "INVALID_DATA_WITHOUT_SEGMENT_TYPE"
        expected = "INVALID_DATA_WITHOUT_SEGMENT_TYPE"
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, segment_types, self.context))

    def test_remove_invalid_prefix_custom_segment_types(self):
        """Test remove_invalid_prefix_from_segment_data with custom segment types."""
        custom_segment_types = ["UNB", "UNH", "CUSTOM"]

        test_data = "PREFIX:CUSTOM+DATA"
        expected = "CUSTOM+DATA"
        self.assertEqual(expected, self.parser.remove_invalid_prefix_from_segment_data(test_data, custom_segment_types, self.context))


if __name__ == '__main__':
    unittest.main()
