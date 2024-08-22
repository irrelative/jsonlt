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

Transformations are executed sequentially in the order they appear in the `transformations` array. This sequential execution allows you to use the results of earlier transformations in subsequent steps, enabling complex, multi-step transformations of your JSON data.

### Common Elements

Most transformations share some common elements:

#### path

- **Type**: String
- **Default**: "."
- **Description**: Specifies the location in the JSON structure where the transformation should be applied. The path uses dot notation to navigate nested structures and must always start with a ".". 
  - "." represents the root of the JSON document.
  - ".field.subfield" would target a nested object.
  - ".array[]" applies the transformation to all elements of an array.
  - ".array[0]" targets a specific array index.

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
  "path": ".user.details",
  "source": "name",
  "target": "fullName"
}
```

This transformation would rename the "name" field to "fullName" within the "user.details" object of the JSON document.

### 3. Rename Transformation

The Rename transformation changes the name of a field in the JSON structure.

#### Inputs

- `type` (required): String, must be "rename"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `source` (required): String, the name of the field to be renamed
- `target` (required): String, the new name for the field

#### Output

The transformation modifies the input JSON by changing the name of the specified field from `source` to `target` at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "personal_info": {
      "first_name": "John",
      "last_name": "Doe"
    }
  }
}
```

Transformation:
```json
{
  "type": "rename",
  "path": ".user.personal_info",
  "source": "first_name",
  "target": "given_name"
}
```

Output JSON:
```json
{
  "user": {
    "personal_info": {
      "given_name": "John",
      "last_name": "Doe"
    }
  }
}
```

In this example, the "first_name" field is renamed to "given_name" within the "user.personal_info" object.

### 4. Reorder Transformation

The Reorder transformation changes the order of fields in a JSON object.

#### Inputs

- `type` (required): String, must be "reorder"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `order` (required): Array of strings, specifies the new order of fields

#### Output

The transformation modifies the input JSON by reordering the fields according to the specified `order` at the location specified by `path`. Fields not mentioned in the `order` array will be placed at the end in their original order.

#### Example

Input JSON:
```json
{
  "user": {
    "personal_info": {
      "last_name": "Doe",
      "first_name": "John",
      "age": 30
    }
  }
}
```

Transformation:
```json
{
  "type": "reorder",
  "path": ".user.personal_info",
  "order": ["first_name", "last_name", "age"]
}
```

Output JSON:
```json
{
  "user": {
    "personal_info": {
      "first_name": "John",
      "last_name": "Doe",
      "age": 30
    }
  }
}
```

In this example, the fields within the "user.personal_info" object are reordered according to the specified order.

### 5. Convert Attribute to Element Transformation

The Convert Attribute to Element transformation changes an attribute of a JSON object into a nested element.

#### Inputs

- `type` (required): String, must be "attribute_to_element"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `source` (required): String, the name of the attribute to be converted
- `target` (required): String, the name of the new element that will contain the attribute

#### Output

The transformation modifies the input JSON by converting the specified attribute into a nested element at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 30
  }
}
```

Transformation:
```json
{
  "type": "attribute_to_element",
  "path": ".user",
  "source": "name",
  "target": "personal_info"
}
```

Output JSON:
```json
{
  "user": {
    "personal_info": {
      "name": "John Doe"
    },
    "age": 30
  }
}
```

In this example, the "name" attribute is converted into a nested "personal_info" element within the "user" object.

### 6. Convert Element to Attribute Transformation

The Convert Element to Attribute transformation changes a nested element of a JSON object into an attribute.

#### Inputs

- `type` (required): String, must be "element_to_attribute"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `source` (required): String, the name of the element to be converted
- `target` (required): String, the name of the new attribute that will contain the element's value

#### Output

The transformation modifies the input JSON by converting the specified nested element into an attribute at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "personal_info": {
      "name": "John Doe"
    },
    "age": 30
  }
}
```

Transformation:
```json
{
  "type": "element_to_attribute",
  "path": ".user",
  "source": "personal_info.name",
  "target": "full_name"
}
```

Output JSON:
```json
{
  "user": {
    "full_name": "John Doe",
    "age": 30
  }
}
```

In this example, the nested "name" element within "personal_info" is converted into a "full_name" attribute of the "user" object.

### 7. Conditional Transformation

The Conditional transformation applies different transformations based on a specified condition.

#### Inputs

- `type` (required): String, must be "conditional"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `condition` (required): Object, specifies the condition to evaluate
  - `operator` (required): String, one of "eq", "ne", "gt", "lt", "ge", "le", "and", "or", "not"
  - `left` (required): String or nested condition object, the left operand or a nested condition
  - `right` (optional): Any value or nested condition object, the right operand (not required for "not" operator)
- `true_transformation` (required): Object, the transformation to apply if the condition is true
- `false_transformation` (optional): Object, the transformation to apply if the condition is false

#### Output

The transformation evaluates the condition and applies either the `true_transformation` or `false_transformation` (if provided) based on the result.

#### Example

Input JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 25
  }
}
```

Transformation:
```json
{
  "type": "conditional",
  "path": ".user",
  "condition": {
    "operator": "gt",
    "left": "age",
    "right": 18
  },
  "true_transformation": {
    "type": "add",
    "target": "status",
    "value": "adult"
  },
  "false_transformation": {
    "type": "add",
    "target": "status",
    "value": "minor"
  }
}
```

Output JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 25,
    "status": "adult"
  }
}
```

In this example, the condition checks if the user's age is greater than 18. Since it is, the `true_transformation` is applied, adding a "status" field with the value "adult". If the age had been 18 or less, the `false_transformation` would have been applied instead, setting the status to "minor".

### 8. Merge Transformation

The Merge transformation combines multiple source fields into a single target field.

#### Inputs

- `type` (required): String, must be "merge"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `sources` (required): Array of strings, specifies the fields to be merged
- `target` (required): String, the name of the new field that will contain the merged data

#### Output

The transformation modifies the input JSON by merging the specified source fields into a single target field at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "age": 30
  }
}
```

Transformation:
```json
{
  "type": "merge",
  "path": ".user",
  "sources": ["first_name", "last_name"],
  "target": "full_name"
}
```

Output JSON:
```json
{
  "user": {
    "full_name": {
      "first_name": "John",
      "last_name": "Doe"
    },
    "age": 30
  }
}
```

In this example, the "first_name" and "last_name" fields are merged into a new "full_name" object within the "user" object. The original source fields are removed after the merge.

### 9. Split Transformation

The Split transformation divides a source field into multiple target fields.

#### Inputs

- `type` (required): String, must be "split"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `source` (required): String, the name of the field to be split
- `targets` (required): Array of strings, specifies the names of the new fields that will contain the split data

#### Output

The transformation modifies the input JSON by splitting the specified source field into multiple target fields at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "full_name": {
      "first": "John",
      "last": "Doe"
    },
    "age": 30
  }
}
```

Transformation:
```json
{
  "type": "split",
  "path": ".user",
  "source": "full_name",
  "targets": ["first_name", "last_name"]
}
```

Output JSON:
```json
{
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "age": 30
  }
}
```

In this example, the "full_name" object is split into separate "first_name" and "last_name" fields within the "user" object. The original "full_name" field is removed after the split.

### 10. Add Element Transformation

The Add Element transformation creates a new field in the JSON structure with a specified value.

#### Inputs

- `type` (required): String, must be "add"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `target` (required): String, the name of the new field to be added
- `value` (required): Any, the value to be assigned to the new field

#### Output

The transformation modifies the input JSON by adding a new field with the specified name and value at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 30
  }
}
```

Transformation:
```json
{
  "type": "add",
  "path": ".user",
  "target": "is_active",
  "value": true
}
```

Output JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 30,
    "is_active": true
  }
}
```

In this example, a new "is_active" field with the value `true` is added to the "user" object.

### 11. Remove Element Transformation

The Remove Element transformation deletes a specified field from the JSON structure.

#### Inputs

- `type` (required): String, must be "remove"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `target` (required): String, the name of the field to be removed

#### Output

The transformation modifies the input JSON by removing the specified field at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 30,
    "temporary_field": "to be removed"
  }
}
```

Transformation:
```json
{
  "type": "remove",
  "path": ".user",
  "target": "temporary_field"
}
```

Output JSON:
```json
{
  "user": {
    "name": "John Doe",
    "age": 30
  }
}
```

In this example, the "temporary_field" is removed from the "user" object.

### 12. Text Modification Transformation

The Text Modification transformation applies various text operations to a specified field in the JSON structure.

#### Inputs

- `type` (required): String, must be "modify_text"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `target` (required): String, the name of the field to be modified
- `modification` (required): String, one of "uppercase", "lowercase", "capitalize", "title", "strip", or "replace"
- `replace_old` (optional): String, required only when `modification` is "replace", specifies the substring to be replaced
- `replace_new` (optional): String, required only when `modification` is "replace", specifies the replacement substring

#### Output

The transformation modifies the input JSON by applying the specified text modification to the target field at the location specified by `path`.

#### Example

Input JSON:
```json
{
  "user": {
    "name": "john doe",
    "email": "JOHN.DOE@EXAMPLE.COM",
    "bio": "  Web developer  "
  }
}
```

Transformations:
```json
[
  {
    "type": "modify_text",
    "path": ".user",
    "target": "name",
    "modification": "title"
  },
  {
    "type": "modify_text",
    "path": ".user",
    "target": "email",
    "modification": "lowercase"
  },
  {
    "type": "modify_text",
    "path": ".user",
    "target": "bio",
    "modification": "strip"
  }
]
```

Output JSON:
```json
{
  "user": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "bio": "Web developer"
  }
}
```

In this example, three text modifications are applied:
1. The "name" field is converted to title case.
2. The "email" field is converted to lowercase.
3. The "bio" field has leading and trailing whitespace removed.

For the "replace" modification, you would use it like this:

```json
{
  "type": "modify_text",
  "path": ".user",
  "target": "name",
  "modification": "replace",
  "replace_old": "john",
  "replace_new": "Jane"
}
```

This would replace "john" with "Jane" in the "name" field.

### 13. Copy Structure Transformation

The Copy Structure transformation creates a copy of a specified part of the JSON structure and applies additional transformations to the copy.

#### Inputs

- `type` (required): String, must be "copy_structure"
- `path` (optional): String, default is ".", specifies where in the JSON structure to apply the transformation
- `modifications` (required): Array of transformation objects, specifies the transformations to apply to the copied structure

#### Output

The transformation creates a copy of the structure at the specified `path` and applies the specified `modifications` to the copy. The original structure remains unchanged.

#### Example

Input JSON:
```json
{
  "user": {
    "name": "John Doe",
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "country": "USA"
    }
  }
}
```

Transformation:
```json
{
  "type": "copy_structure",
  "path": ".user",
  "modifications": [
    {
      "type": "rename",
      "path": ".",
      "source": "name",
      "target": "full_name"
    },
    {
      "type": "remove",
      "path": ".address",
      "target": "street"
    }
  ]
}
```

Output JSON:
```json
{
  "user": {
    "name": "John Doe",
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "country": "USA"
    },
    "full_name": "John Doe",
    "address": {
      "city": "Anytown",
      "country": "USA"
    }
  }
}
```

In this example, the entire "user" structure is copied. In the copy, the "name" field is renamed to "full_name", and the "street" field is removed from the "address" object. The original "user" structure remains unchanged, while the modified copy is added to the same level.
