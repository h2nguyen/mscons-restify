import os
import json

from fastapi.testclient import TestClient


def test_parse_mscons_raw_format(client: TestClient):
    """Test that the /parse-raw-format endpoint returns the expected response."""
    # Read the sample MSCONS data from a file
    mscons_file_path = "samples/mscons-message-example.txt" \
        if os.path.exists("samples/mscons-message-example.txt") \
        else "tests/samples/mscons-message-example.txt"
    with open(mscons_file_path, "r") as f:
        mscons_data = f.read()

    # Read the expected response from the JSON file
    expected_response_path = "samples/mscons-message-example-expected-response.json" \
        if os.path.exists("samples/mscons-message-example-expected-response.json") \
        else "tests/samples/mscons-message-example-expected-response.json"
    with open(expected_response_path, "r") as f:
        expected_response = json.load(f)

    # Test the endpoint with plain text
    response = client.post(
        "/parse-raw-format",
        content=mscons_data,
        headers={"Content-Type": "text/plain"}
    )

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response matches the expected JSON
    assert response.json() == expected_response
