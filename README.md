# JSON Language Transformation

This document outlines the functionalities required for a JSON-to-JSON transformation language. The goal is to provide a comprehensive set of transformation capabilities that can be applied to convert one JSON format to another.

## Example

Here's a simple example of how JSONLT can be used to transform JSON data:

Input JSON:
```json
{
  "person": {
    "firstName": "John",
    "lastName": "Doe",
    "age": 30
  }
}
```

JSONLT Configuration:
```json
{
  "transformations": [
    {
      "type": "rename",
      "path": ".person",
      "source": "firstName",
      "target": "givenName"
    },
    {
      "type": "rename",
      "path": ".person",
      "source": "lastName",
      "target": "familyName"
    },
    {
      "type": "concat",
      "path": ".person",
      "sources": ["givenName", "familyName"],
      "target": "fullName",
      "delimiter": " "
    }
  ]
}
```

Output JSON:
```json
{
  "person": {
    "givenName": "John",
    "familyName": "Doe",
    "age": 30,
    "fullName": "John Doe"
  }
}
```

This example demonstrates renaming fields, adding a new field, and concatenating values.


## Implementations

Initial versions of this package will focus on a python implementation. When functionality is stable, other implementations in
other langauges will be considered.


## Installation

To install JSONLT, you can use pip:

```sh
pip install jsonlt
```

Alternatively, you can install from source:

```sh
git clone https://github.com/your-repo/jsonlt.git
cd jsonlt
python setup.py install
```

## Usage

JSONLT can be used both programmatically and via a command-line interface (CLI).

### Programmatic Usage

Here's an example of how to use JSONLT in your Python code:

```python
import jsonlt

input_data = {"name": "Bob"}

jsonlt_config = {
    "transformations": [
        {"type": "rename", "path": ".", "source": "name", "target": "fullName"}
    ]
}

output = jsonlt.transform(input_data, jsonlt_config)
print(output)
# Output: {'fullName': 'Bob'}
```

### Command-Line Interface

JSONLT also provides a CLI for easy use:

```sh
jsonlt --help

usage: jsonlt [-h] [-i] [-o OUTPUT] [input] [config]

JSONLT: JSON Transformation Tool

positional arguments:
  input                 Input JSON file
  config                JSONLT configuration file

options:
  -h, --help            show this help message and exit
  -i, --interactive     Run in interactive mode
  -o OUTPUT, --output OUTPUT
                        Output JSON file (default: stdout)
```

Example usage:

```sh
jsonlt input.json config.json -o output.json
```

This command will transform the JSON in `input.json` according to the configuration in `config.json` and save the result to `output.json`.

## Documentation
For detailed usage instructions and examples of each transformation type, please refer to the [Usage Guide](docs/usage.md).

## Functionality

* **Element renaming**. Rename keys in the object.
* **Attribute renaming**. Rename attributes within nested objects.
* **Element reordering**. Change the order of key-value pairs.
* **Attribute to element conversion**. Convert an attribute to a nested object.
* **Element to attribute conversion**. Convert a nested object to an attribute.
* **Conditional processing**. Apply transformations based on conditions.
* **Merging or splitting elements**. Combine or separate key-value pairs.
* **Adding new elements or attributes**. Introduce new key-value pairs.
* **Removing elements or attributes**. Remove specific key-value pairs.
* **Changing text content**. Modify text values.
* **Copying structure with modifications**. Duplicate and modify the JSON structure.
* **Grouping elements**. Group array elements based on common attributes.
* **Concatenation**. Combine multiple fields into a single field.
