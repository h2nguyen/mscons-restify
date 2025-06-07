import os
import unittest

from msconsparser.libs.edifactmsconsparser.edifact_mscons_parser import EdifactMSCONSParser


class TestSimpleParser(unittest.TestCase):
    """A simple test case to demonstrate testing in this project."""

    def setUp(self):
        self.parser = EdifactMSCONSParser()

    def test_parse_sample_file(self):
        """Test that the parser can parse the sample file."""
        # Read the sample file
        mscons_file_path = "samples/mscons-message-example.txt" \
            if os.path.exists("samples/mscons-message-example.txt") \
            else "tests/samples/mscons-message-example.txt"

        with open(mscons_file_path, encoding='utf-8') as f:
            edifact_data = f.read()

        # Parse the data
        mscons_obj = self.parser.parse(edifact_data)

        # Verify some basic properties
        self.assertIsNotNone(mscons_obj)
        self.assertEqual(mscons_obj.unz_nutzdaten_endsegment.datenaustauschzaehler, 2)
        self.assertEqual(len(mscons_obj.unh_unt_nachrichten), 2)


if __name__ == '__main__':
    unittest.main()
