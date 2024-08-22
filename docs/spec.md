# JSONLT Specification

## Introduction

JSONLT (JSON Transformation Language) is a declarative language designed for transforming JSON data structures. It provides a flexible and powerful way to modify, restructure, and manipulate JSON data without writing complex code.

JSONLT is used for various purposes, including:

1. Data integration: Transforming data between different JSON schemas or formats.
2. API response modification: Adjusting the structure of API responses to meet specific client needs.
3. Data cleaning and normalization: Standardizing JSON data from various sources.
4. Complex data transformations: Performing advanced operations like conditional transformations, merging, splitting, and grouping of JSON elements.

The JSONLT specification defines a set of transformation operations that can be applied to JSON data in a predictable and consistent manner. These transformations are described using a JSON-based configuration, making it easy to read, write, and integrate with existing JSON-based systems.

## 1. JSONLT Object

The top-level JSONLT object is a JSON object with the following structure:

```json
{
  "transformations": [
    // Array of transformation objects
  ]
}
```

### Properties

- `transformations` (required): An array of transformation objects that define the sequence of transformations to be applied to the input JSON data.

Each transformation object in the `transformations` array represents a specific operation to be performed on the JSON data. The order of the transformations in the array determines the order in which they will be applied.

## 2. Transformations

Transformations are the core components of JSONLT. Each transformation is represented by a JSON object that specifies the type of operation to perform and any necessary parameters.

### Common Elements

Most transformations share some common elements:

#### path

- **Type**: String
- **Default**: "."
- **Description**: Specifies the location in the JSON structure where the transformation should be applied. The path uses dot notation to navigate nested structures. 
  - "." represents the root of the JSON document.
  - "field.subfield" would target a nested object.
  - "array[]" applies the transformation to all elements of an array.
  - "array[0]" targets a specific array index.

#### source

- **Type**: String
- **Description**: Identifies the field or element in the input JSON that will be transformed or used as input for the transformation.

#### target

- **Type**: String
- **Description**: Specifies the field or element in the output JSON where the result of the transformation will be stored.

### Example

Here's an example of a transformation using these common elements:

```json
{
  "type": "rename",
  "path": "user.details",
  "source": "name",
  "target": "fullName"
}
```

This transformation would rename the "name" field to "fullName" within the "user.details" object of the JSON document.
