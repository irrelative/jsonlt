# JSONLT Transformations Usage Guide

This document provides an overview of each transformation type available in JSONLT, along with examples of how to use them.

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

Remember that you can use the "path" field in each transformation to specify where in your JSON structure the transformation should be applied. The default "." applies the transformation at the root level.
