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

```sh
python setup.py install
```


## Usage

Once installed the library can be used programmatically like so:

```python
import jsonlt

inp = {"name": "Bob"}

jlt = {
    "transformations": [
        {"type": "rename", "path": ".", "source": "name", "target": "new"}
    ]
}

output = jsonlt.transform(inp, jlt)
print(output)
# {'new': 'Bob'}

```

There's also a CLI `jsonlt`:

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
