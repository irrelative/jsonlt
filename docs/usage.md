# JSONLT Transformations Usage Guide

This document provides an overview of each transformation type available in JSONLT, along with examples of how to use them.

## End-to-End Example

Here's a comprehensive example demonstrating multiple JSONLT transformations:

Input JSON:
```json
{
  "person": {
    "firstName": "john",
    "lastName": "doe",
    "age": 30,
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "country": "USA"
    },
    "hobbies": ["reading", "cycling", "photography"]
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
      "delimiter": " ",
      "target": "fullName"
    },
    {
      "type": "modify_text",
      "path": ".person",
      "target": "fullName",
      "modification": "title"
    },
    {
      "type": "conditional",
      "path": ".person",
      "condition": {
        "operator": "gt",
        "left": "age",
        "right": 18
      },
      "true_transformation": {
        "type": "add",
        "path": ".",
        "target": "isAdult",
        "value": true
      },
      "false_transformation": {
        "type": "add",
        "path": ".",
        "target": "isAdult",
        "value": false
      }
    },
    {
      "type": "rename",
      "path": ".person.address",
      "source": "country",
      "target": "countryCode"
    },
    {
      "type": "reorder",
      "path": ".person",
      "order": ["fullName", "age", "isAdult", "address", "hobbies"]
    }
  ]
}
```

Output JSON:
```json
{
  "person": {
    "fullName": "John Doe",
    "age": 30,
    "isAdult": true,
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "countryCode": "USA"
    },
    "hobbies": ["reading", "cycling", "photography"]
  }
}
```

This example demonstrates the following transformations:
1. Renaming "firstName" to "givenName" and "lastName" to "familyName"
2. Merging "givenName" and "familyName" into "fullName"
3. Modifying the text of "fullName" to title case
4. Conditionally adding an "isAdult" field based on the age
5. Converting the "country" element to a "countryCode" attribute in the address
6. Reordering the fields in the "person" object

Now, let's dive into each transformation type in detail.

## 1. Rename Transformation

The rename transformation allows you to change the name of a key in your JSON data.

Example:
```json
{
  "type": "rename",
  "path": ".",
  "source": "old_name",
  "target": "new_name"
}
```

This will rename the key "old_name" to "new_name" at the root level of your JSON.

## 2. Reorder Transformation

The reorder transformation allows you to change the order of keys in your JSON data.

Example:
```json
{
  "type": "reorder",
  "path": ".",
  "order": ["name", "age", "city"]
}
```

This will reorder the keys at the root level to match the specified order.

## 3. Attribute to Element Transformation

This transformation converts an attribute to a nested element.

Example:
```json
{
  "type": "attribute_to_element",
  "path": ".",
  "source": "age",
  "target": "person_age"
}
```

This will convert `{"age": 30}` to `{"person_age": {"age": 30}}`.

## 4. Element to Attribute Transformation

This transformation converts a nested element to an attribute.

Example:
```json
{
  "type": "element_to_attribute",
  "path": ".",
  "source": "person_age",
  "target": "age"
}
```

This will convert `{"person_age": {"age": 30}}` to `{"age": 30}`.

## 5. Conditional Transformation

The conditional transformation applies different transformations based on a condition.

Example:
```json
{
  "type": "conditional",
  "path": ".",
  "condition": {
    "operator": "eq",
    "left": "status",
    "right": "active"
  },
  "true_transformation": {
    "type": "add",
    "path": ".",
    "target": "is_active",
    "value": true
  },
  "false_transformation": {
    "type": "add",
    "path": ".",
    "target": "is_active",
    "value": false
  }
}
```

This will add an "is_active" field based on the value of the "status" field.

## 6. Merge Transformation

The merge transformation combines multiple fields into a single field.

Example:
```json
{
  "type": "merge",
  "path": ".",
  "sources": ["first_name", "last_name"],
  "target": "full_name"
}
```

This will merge "first_name" and "last_name" into a single "full_name" field.

## 7. Split Transformation

The split transformation separates a single field into multiple fields.

Example:
```json
{
  "type": "split",
  "path": ".",
  "source": "full_name",
  "targets": ["first_name", "last_name"]
}
```

This will split the "full_name" field into separate "first_name" and "last_name" fields.

## 8. Add Element Transformation

This transformation adds a new element or attribute to your JSON data.

Example:
```json
{
  "type": "add",
  "path": ".",
  "target": "new_field",
  "value": "new value"
}
```

This will add a new field "new_field" with the value "new value" at the root level.

## 9. Remove Element Transformation

This transformation removes an element or attribute from your JSON data.

Example:
```json
{
  "type": "remove",
  "path": ".",
  "target": "unwanted_field"
}
```

This will remove the "unwanted_field" from the root level of your JSON.

## 10. Modify Text Transformation

This transformation allows you to modify text content in various ways.

Example:
```json
{
  "type": "modify_text",
  "path": ".",
  "target": "name",
  "modification": "uppercase"
}
```

This will convert the "name" field to uppercase.

## 11. Copy Structure Transformation

This transformation creates a copy of the entire structure with specified modifications.

Example:
```json
{
  "type": "copy_structure",
  "path": ".",
  "modifications": [
    {
      "type": "add",
      "path": ".",
      "target": "copied",
      "value": true
    }
  ]
}
```

This will create a copy of the entire structure and add a "copied" field set to true.

## 12. Group Transformation

This transformation groups elements based on a specified field.

Example:
```json
{
  "type": "group",
  "path": ".",
  "source": "employees",
  "target": "departments",
  "group_by": "department"
}
```

This will group the "employees" array into a "departments" object, with each department as a key containing an array of employees in that department.

## 13. Concat Transformation

This transformation concatenates multiple fields into a single field.

Example:
```json
{
  "type": "concat",
  "path": ".",
  "sources": ["firstName", "lastName"],
  "target": "fullName",
  "delimiter": " "
}
```

This will concatenate the "firstName" and "lastName" fields into a single "fullName" field, using a space as the delimiter.

Remember that you can use the "path" field in each transformation to specify where in your JSON structure the transformation should be applied. The "path" value must always start with a dot (`.`). For example:

- `.` applies the transformation at the root level (default)
- `.person` applies the transformation to the "person" object at the root level
- `.person.address` applies the transformation to the "address" object within the "person" object

This ensures that all paths are relative to the root of the JSON document.
