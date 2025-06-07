import unittest

from msconsparser.libs.edifactmsconsparser.utils.mscons_utils import MSCONSUtils


class TestMSCONSUtils(unittest.TestCase):
    """Test case for the MSCONSUtils class."""

    def test_split_segments_with_multiple_segments(self):
        """Test splitting a string with multiple segments."""
        # Arrange
        input_string = "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345'UNH+12345+MSCONS:D:96A:UN:EAN005'BGM+7+MSI5422+9'"

        # Act
        result = MSCONSUtils.split_segments(input_string)

        # Assert
        self.assertEqual(len(result), 4)  # 3 segments + empty string after last segment terminator
        self.assertEqual(result[0], "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345")
        self.assertEqual(result[1], "UNH+12345+MSCONS:D:96A:UN:EAN005")
        self.assertEqual(result[2], "BGM+7+MSI5422+9")
        self.assertEqual(result[3], "")  # Empty string after last segment terminator

    def test_split_segments_with_empty_string(self):
        """Test splitting an empty string."""
        # Arrange
        input_string = ""

        # Act
        result = MSCONSUtils.split_segments(input_string)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "")

    def test_split_segments_with_no_terminators(self):
        """Test splitting a string with no segment terminators."""
        # Arrange
        input_string = "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ+230101:1200+12345"

        # Act
        result = MSCONSUtils.split_segments(input_string)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], input_string)

    def test_split_components_with_multiple_components(self):
        """Test splitting a string with multiple components."""
        # Arrange
        input_string = "UNOC:3:TEST:EXAMPLE"

        # Act
        result = MSCONSUtils.split_components(input_string)

        # Assert
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "UNOC")
        self.assertEqual(result[1], "3")
        self.assertEqual(result[2], "TEST")
        self.assertEqual(result[3], "EXAMPLE")

    def test_split_components_with_escaped_separator(self):
        """Test splitting a string with escaped component separators."""
        # Arrange
        input_string = "UNOC?:3:TEST?::EXAMPLE"

        # Act
        result = MSCONSUtils.split_components(input_string)

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "UNOC:3")
        self.assertEqual(result[1], "TEST:")
        self.assertEqual(result[2], "EXAMPLE")

    def test_split_components_with_empty_string(self):
        """Test splitting an empty string into components."""
        # Arrange
        input_string = ""

        # Act
        result = MSCONSUtils.split_components(input_string)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "")

    def test_split_components_with_no_separators(self):
        """Test splitting a string with no component separators."""
        # Arrange
        input_string = "UNOC"

        # Act
        result = MSCONSUtils.split_components(input_string)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "UNOC")

    def test_split_elements_with_multiple_elements(self):
        """Test splitting a string with multiple elements."""
        # Arrange
        input_string = "UNB+UNOC:3+SENDER:ZZ+RECIPIENT:ZZ"

        # Act
        result = MSCONSUtils.split_elements(input_string)

        # Assert
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "UNB")
        self.assertEqual(result[1], "UNOC:3")
        self.assertEqual(result[2], "SENDER:ZZ")
        self.assertEqual(result[3], "RECIPIENT:ZZ")

    def test_split_elements_with_escaped_separator(self):
        """Test splitting a string with escaped element separators."""
        # Arrange
        input_string = "UNB+UNOC:3+SENDER?+VALUE:ZZ+RECIPIENT:ZZ"

        # Act
        result = MSCONSUtils.split_elements(input_string)

        # Assert
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "UNB")
        self.assertEqual(result[1], "UNOC:3")
        self.assertEqual(result[2], "SENDER+VALUE:ZZ")
        self.assertEqual(result[3], "RECIPIENT:ZZ")

    def test_split_elements_with_empty_string(self):
        """Test splitting an empty string into elements."""
        # Arrange
        input_string = ""

        # Act
        result = MSCONSUtils.split_elements(input_string)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "")

    def test_split_elements_with_no_separators(self):
        """Test splitting a string with no element separators."""
        # Arrange
        input_string = "UNB"

        # Act
        result = MSCONSUtils.split_elements(input_string)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "UNB")

    def test_split_elements_with_consecutive_separators(self):
        """Test splitting a string with consecutive element separators."""
        # Arrange
        input_string = "UNB++SENDER:ZZ++RECIPIENT:ZZ"

        # Act
        result = MSCONSUtils.split_elements(input_string)

        # Assert
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], "UNB")
        self.assertEqual(result[1], "")
        self.assertEqual(result[2], "SENDER:ZZ")
        self.assertEqual(result[3], "")
        self.assertEqual(result[4], "RECIPIENT:ZZ")

    def test_split_components_with_consecutive_separators(self):
        """Test splitting a string with consecutive component separators."""
        # Arrange
        input_string = "UNOC::TEST::EXAMPLE"

        # Act
        result = MSCONSUtils.split_components(input_string)

        # Assert
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], "UNOC")
        self.assertEqual(result[1], "")
        self.assertEqual(result[2], "TEST")
        self.assertEqual(result[3], "")
        self.assertEqual(result[4], "EXAMPLE")

    def test_escape_at_end_of_string(self):
        """Test handling of escape character at the end of the string."""
        # Arrange
        input_string = "UNOC:3:TEST?"

        # Act
        result = MSCONSUtils.split_components(input_string)

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "UNOC")
        self.assertEqual(result[1], "3")
        self.assertEqual(result[2], "TEST?")  # Escape at end is preserved as is


if __name__ == '__main__':
    unittest.main()