# JSON Language Transformation
This document outlines the functionalities required for a JSON-to-JSON transformation language. The goal is to provide a comprehensive set of transformation capabilities that can be applied to convert one JSON format to another.


## Functionality

1. **Element Renaming**

    Description: Rename keys within JSON objects.

    Example: Rename "oldKey": "value" to "newKey": "value".
2. **Attribute Renaming**

    Description: Rename attributes within nested JSON objects.

    Example: { "object": { "oldAttr": "value" } } to { "object": { "newAttr": "value" } }.
3. **Element Reordering**

    Description: Change the order of key-value pairs within a JSON object.

    Example: Change { "key1": "value1", "key2": "value2" } to { "key2": "value2", "key1": "value1" }.
4. **Attribute to Element Conversion**

    Description: Convert a JSON attribute (key-value pair) into a nested object.

    Example: { "object": { "attr": "value" } } to { "object": { "attr": { "value": "value" } } }.
5. **Element to Attribute Conversion**

    Description: Convert a nested JSON object into an attribute (key-value pair).

    Example: { "object": { "child": { "value": "value" } } } to { "object": { "child": "value" } }.
6. **Conditional Processing**

    Description: Apply different transformations based on specific conditions within the JSON structure.

    Example: Transform the JSON structure differently based on the value of a key.
7. **Merging or Splitting Elements**

    Description: Combine multiple JSON objects or key-value pairs into one, or split a single key-value pair into multiple.

    Example: Merge { "firstName": "John", "lastName": "Doe" } into { "fullName": "John Doe" }, or split { "fullName": "John Doe" } into { "firstName": "John", "lastName": "Doe" }.
8. **Adding New Elements or Attributes**

    Description: Introduce new key-value pairs or nested objects not present in the original JSON.

    Example: Add a "timestamp": "2024-08-21T12:34:56" to the JSON object.
9. **Removing Elements or Attributes**

    Description: Remove specific key-value pairs or nested objects from the JSON structure.

    Example: Remove "unwantedKey": "value" from the JSON object.
10. **Changing Text Content**

    Description: Modify the text content of values within JSON key-value pairs.

    Example: Convert the value of a key from lowercase to uppercase.
11. **Copying the Entire Structure with Modifications**

    Description: Copy the entire JSON structure while applying specific modifications to certain keys or values.

    Example: Duplicate the original JSON while altering specified keys or attributes.
12. **Grouping Elements**

    Description: Group elements within a JSON array based on common values or attributes.

    Example: Group objects in an array by a shared attribute, such as grouping users by their role.
