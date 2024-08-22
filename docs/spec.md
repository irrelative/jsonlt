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
