import json
import os

from jsonlt import transform

def find_testfiles_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        if 'testfiles' in os.listdir(current_dir):
            return os.path.join(current_dir, 'testfiles')
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise FileNotFoundError("Could not find 'testfiles' folder")
        current_dir = parent_dir


def test_json_files():
    test_folder = find_testfiles_folder()
    for filename in os.listdir(test_folder):
        if filename.endswith(".json"):
            with open(os.path.join(test_folder, filename), "r") as file:
                test_case = json.load(file)

                input_data = test_case["input"]
                jsonlt_conf = test_case["jsonlt"]
                expected_output = test_case["output"]

                result = transform(input_data, jsonlt_conf)

                assert result == expected_output, f"Test failed for {filename}"
