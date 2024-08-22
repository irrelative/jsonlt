import argparse
import json
import sys

from .xform import jsonlt_transform


def interactive_mode():
    print("Enter your JSON input (press Enter twice to finish):")
    input_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        input_lines.append(line)
    input_data = json.loads("\n".join(input_lines))

    print("\nEnter your JSONLT configuration (press Enter twice to finish):")
    config_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        config_lines.append(line)
    jsonlt_config = json.loads("\n".join(config_lines))

    result = jsonlt_transform(input_data, jsonlt_config)
    print("\nTransformed JSON:")
    json.dump(result, sys.stdout, indent=2)


def main():
    parser = argparse.ArgumentParser(description="JSONLT: JSON Transformation Tool")
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("input", nargs="?", help="Input JSON file")
    parser.add_argument("config", nargs="?", help="JSONLT configuration file")
    parser.add_argument("-o", "--output", help="Output JSON file (default: stdout)")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    if not args.input or not args.config:
        parser.error("Input and config files are required when not in interactive mode")

    try:
        with open(args.input, "r") as f:
            input_data = json.load(f)

        with open(args.config, "r") as f:
            jsonlt_config = json.load(f)

        result = jsonlt_transform(input_data, jsonlt_config)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
        else:
            json.dump(result, sys.stdout, indent=2)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
