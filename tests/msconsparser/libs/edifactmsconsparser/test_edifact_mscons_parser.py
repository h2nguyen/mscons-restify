import unittest
from unittest.mock import patch, MagicMock

from msconsparser.libs.edifactmsconsparser.edifact_mscons_parser import EdifactMSCONSParser
from msconsparser.libs.edifactmsconsparser.utils import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentType, SegmentGroup, EdifactInterchange


class TestEdifactMSCONSParser(unittest.TestCase):
    """Test case for the EdifactMSCONSParser class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = EdifactMSCONSParser()

    def test_init(self):
        """Test that the parser initializes correctly."""
        self.assertIsNotNone(self.parser._EdifactMSCONSParser__handler_factory)
        # Context is private, so we don't test it directly

    def test_parse_empty_string(self):
        """Test parsing an empty string."""
        # Act
        result = self.parser.parse("")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(1, self.parser._EdifactMSCONSParser__context.segment_count)

    @patch('msconsparser.libs.edifactmsconsparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_segments')
    @patch('msconsparser.libs.edifactmsconsparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_elements')
    @patch('msconsparser.libs.edifactmsconsparser.utils.edifact_syntax_helper.EdifactSyntaxHelper.split_components')
    def test_parse_with_mocked_utils(self, mock_split_components, mock_split_elements, mock_split_segments):
        """Test parsing with mocked utility methods."""
        # Arrange
        mock_split_segments.return_value = ["UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345"]
        mock_split_elements.return_value = ["UNB", "UNOC:3", "SENDER:ZZ", "RECIPIENT:ZZ", "230101:1200", "12345"]
        mock_split_components.return_value = ["UNB"]

        # Mock the handler factory and handler
        self.parser._EdifactMSCONSParser__handler_factory = MagicMock()
        mock_handler = MagicMock()
        self.parser._EdifactMSCONSParser__handler_factory.get_handler.return_value = mock_handler

        # Act
        result = self.parser.parse("test_data")

        # Assert
        self.assertIsNotNone(result)
        mock_split_segments.assert_called_once()
        mock_split_elements.assert_called_once()
        mock_split_components.assert_called_once()
        mock_handler.handle.assert_called_once()
        self.assertEqual(1, self.parser._EdifactMSCONSParser__context.segment_count)

    def test_parse_with_sample_data(self):
        """Test parsing with a simple sample data string."""
        # Arrange
        sample_data = "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345'UNH+12345+MSCONS:D:96A:UN:EAN005'"

        # Act
        result = self.parser.parse(sample_data)

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, EdifactInterchange)
        # Additional assertions would depend on the expected structure of the result

    def test_get_segment_group_with_empty_segment_type(self):
        """Test get_segment_group with an empty segment type."""
        # Act
        result = EdifactMSCONSParser.get_segment_group("", None)

        # Assert
        self.assertIsNone(result)

    def test_get_segment_group_with_dtm(self):
        """Test get_segment_group with DTM segment type."""
        # Arrange
        current_group = None

        # Act
        result = EdifactMSCONSParser.get_segment_group(SegmentType.DTM, current_group)

        # Assert
        self.assertEqual(current_group, result)

    def test_get_segment_group_with_rff(self):
        """Test get_segment_group with RFF segment type in different contexts."""
        # Test RFF in No group
        result = EdifactMSCONSParser.get_segment_group(SegmentType.RFF, None)
        self.assertEqual(SegmentGroup.SG1, result)

        # Test RFF in SG1
        result = EdifactMSCONSParser.get_segment_group(SegmentType.RFF, SegmentGroup.SG1)
        self.assertEqual(SegmentGroup.SG1, result)

        # Test RFF in SG6
        result = EdifactMSCONSParser.get_segment_group(SegmentType.RFF, SegmentGroup.SG6)
        self.assertEqual(SegmentGroup.SG7, result)

        # Test RFF in SG7
        result = EdifactMSCONSParser.get_segment_group(SegmentType.RFF, SegmentGroup.SG7)
        self.assertEqual(SegmentGroup.SG7, result)

    def test_get_segment_group_with_nad(self):
        """Test get_segment_group with NAD segment type in different contexts."""
        # Test NAD in SG1
        result = EdifactMSCONSParser.get_segment_group(SegmentType.NAD, SegmentGroup.SG1)
        self.assertEqual(SegmentGroup.SG2, result)

        # Test NAD in SG4
        result = EdifactMSCONSParser.get_segment_group(SegmentType.NAD, SegmentGroup.SG4)
        self.assertEqual(SegmentGroup.SG2, result)

        # Test NAD in no group
        result = EdifactMSCONSParser.get_segment_group(SegmentType.NAD, None)
        self.assertEqual(SegmentGroup.SG5, result)

    def test_get_segment_group_with_other_types(self):
        """Test get_segment_group with other segment types."""
        # Test CTA
        result = EdifactMSCONSParser.get_segment_group(SegmentType.CTA, None)
        self.assertEqual(SegmentGroup.SG4, result)

        # Test COM
        result = EdifactMSCONSParser.get_segment_group(SegmentType.COM, None)
        self.assertEqual(SegmentGroup.SG4, result)

        # Test LOC
        result = EdifactMSCONSParser.get_segment_group(SegmentType.LOC, None)
        self.assertEqual(SegmentGroup.SG6, result)

        # Test CCI
        result = EdifactMSCONSParser.get_segment_group(SegmentType.CCI, None)
        self.assertEqual(SegmentGroup.SG8, result)

        # Test LIN
        result = EdifactMSCONSParser.get_segment_group(SegmentType.LIN, None)
        self.assertEqual(SegmentGroup.SG9, result)

        # Test PIA
        result = EdifactMSCONSParser.get_segment_group(SegmentType.PIA, None)
        self.assertEqual(SegmentGroup.SG9, result)

        # Test QTY
        result = EdifactMSCONSParser.get_segment_group(SegmentType.QTY, None)
        self.assertEqual(SegmentGroup.SG10, result)

        # Test STS
        result = EdifactMSCONSParser.get_segment_group(SegmentType.STS, None)
        self.assertEqual(SegmentGroup.SG10, result)

    def test_get_segment_group_with_unknown_type(self):
        """Test get_segment_group with an unknown segment type."""
        # Act
        result = EdifactMSCONSParser.get_segment_group("UNKNOWN", None)

        # Assert
        self.assertEqual(None, result)

    @patch(
        'msconsparser.libs.edifactmsconsparser.converters.unb_segment_converter.EdifactSyntaxHelper.split_components')
    def test_parse_with_una_segment(self, mock_split_components):
        """Test parsing with a UNA segment at the beginning of the file."""
        # Arrange
        sample_data = "UNA;*%? 'UNB*UNOC;3*SENDER;ZZ*RECIPIENT;ZZ*230101;1200*12345'"

        # Mock the split_components method to return the expected values
        mock_split_components.side_effect = [
            ["UNOC", "3"],  # syntax_info
            ["SENDER", "ZZ"],  # absender_info
            ["RECIPIENT", "ZZ"],  # empfaenger_info
            ["230101", "1200"],  # erstellung_info
            ["12345"]  # datenaustauschreferenz
        ]

        # Act
        result = self.parser.parse(sample_data)

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, EdifactInterchange)
        self.assertIsNotNone(result.una_service_string_advice)
        self.assertEqual(";", result.una_service_string_advice.component_separator)
        self.assertEqual("*", result.una_service_string_advice.element_separator)
        self.assertEqual("%", result.una_service_string_advice.decimal_mark)
        self.assertEqual("?", result.una_service_string_advice.release_character)
        self.assertEqual(" ", result.una_service_string_advice.reserved)
        self.assertEqual("'", result.una_service_string_advice.segment_terminator)

        # Verify that EdifactSyntaxHelper methods return the correct values from the context
        context = self.parser._EdifactMSCONSParser__context
        self.assertEqual(";", EdifactSyntaxHelper.get_component_separator(context))
        self.assertEqual("*", EdifactSyntaxHelper.get_element_separator(context))
        self.assertEqual("%", EdifactSyntaxHelper.get_decimal_mark(context))
        self.assertEqual("?", EdifactSyntaxHelper.get_release_indicator(context))
        self.assertEqual(" ", EdifactSyntaxHelper.get_reserved_indicator(context))
        self.assertEqual("'", EdifactSyntaxHelper.get_segment_terminator(context))


if __name__ == '__main__':
    unittest.main()
