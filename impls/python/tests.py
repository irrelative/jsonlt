import json
import os

from xform import jsonlt_transform


def test_json_files():
    test_folder = "../../tests"
    for filename in os.listdir(test_folder):
        if filename.endswith(".json"):
            with open(os.path.join(test_folder, filename), "r") as file:
                test_case = json.load(file)

                input_data = test_case["input"]
                jsonlt_conf = test_case["jsonlt"]
                expected_output = test_case["output"]

                result = jsonlt_transform(input_data, jsonlt_conf)

                assert result == expected_output, f"Test failed for {filename}"
