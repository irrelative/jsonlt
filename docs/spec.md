# JSONLT Specification

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
