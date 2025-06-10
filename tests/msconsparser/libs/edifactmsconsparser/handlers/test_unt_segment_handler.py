import unittest
from unittest.mock import MagicMock

from msconsparser.libs.edifactmsconsparser.wrappers.segments import ParsingContext, EdifactMSconsMessage, SegmentUNT
from msconsparser.libs.edifactmsconsparser.converters import UNTSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers.unt_segment_handler import UNTSegmentHandler


class TestUNTSegmentHandler(unittest.TestCase):
    """Test case for the UNTSegmentHandler class."""

    def setUp(self):
        """Set up the test case."""
        self.handler = UNTSegmentHandler()
        self.context = ParsingContext()
        self.context.current_message = EdifactMSconsMessage()
        self.segment = SegmentUNT()

    def test_init_creates_with_correct_converter(self):
        """Test that the handler initializes with the correct converter."""
        self.assertIsInstance(self.handler.converter, UNTSegmentConverter)

    def test_update_context_updates_context_correctly(self):
        """Test that _update_context updates the context correctly."""
        # Arrange
        current_segment_group = None

        # Act
        self.handler._update_context(self.segment, current_segment_group, self.context)

        # Assert
        # The specific assertion will depend on the handler implementation
        # This is a placeholder that should be updated for each handler
        self.assertIsNotNone(self.context.current_message)

    def test_can_handle_returns_true_when_current_message_exists(self):
        """Test that _can_handle returns True when current_message exists."""
        # Act
        result = self.handler._can_handle(self.context)

        # Assert
        self.assertTrue(result)

    def test_can_handle_returns_false_when_current_message_does_not_exist(self):
        """Test that _can_handle returns False when current_message does not exist."""
        # Arrange
        self.context.current_message = None

        # Act
        result = self.handler._can_handle(self.context)

        # Assert
        self.assertFalse(result)

    def test_handle_calls_convert_and_update_context(self):
        """Test that handle calls convert and _update_context."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "example", "data"]
        last_segment_type = None
        current_segment_group = None
        
        # Mock the converter's convert method to return a known segment
        self.handler.converter.convert = MagicMock(return_value=self.segment)
        
        # Mock the _update_context method to verify it's called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler.converter.convert.assert_called_once_with(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group
        )
        self.handler._update_context.assert_called_once_with(self.segment, current_segment_group, self.context)

    def test_handle_does_not_call_convert_when_can_handle_returns_false(self):
        """Test that handle does not call convert when _can_handle returns False."""
        # Arrange
        line_number = 1
        element_components = ["UNT", "example", "data"]
        last_segment_type = None
        current_segment_group = None
        self.context.current_message = None  # This will make _can_handle return False
        
        # Mock the converter's convert method to verify it's not called
        self.handler.converter.convert = MagicMock()
        
        # Mock the _update_context method to verify it's not called
        self.handler._update_context = MagicMock()

        # Act
        self.handler.handle(line_number, element_components, last_segment_type, current_segment_group, self.context)

        # Assert
        self.handler.converter.convert.assert_not_called()
        self.handler._update_context.assert_not_called()


if __name__ == '__main__':
    unittest.main()
