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

JSONLT is currently implemented in Python and JavaScript. This README focuses on the JavaScript implementation.

## Installation

To install the JavaScript version of JSONLT, you can use npm:

```sh
npm install jsonlt
```

Alternatively, you can include the built JavaScript file directly in your HTML:

```html
<script src="path/to/jsonlt.js"></script>
```

## Usage

JSONLT can be used both in Node.js and in the browser.

### Node.js Usage

Here's an example of how to use JSONLT in your Node.js code:

```javascript
const JSONLT = require('jsonlt');

const inputData = { name: "Bob" };

const jsonltConfig = {
    transformations: [
        { type: "rename", path: ".", source: "name", target: "fullName" }
    ]
};

const output = JSONLT.transform(inputData, jsonltConfig);
console.log(output);
// Output: { fullName: 'Bob' }
```

### Browser Usage

When using JSONLT in the browser, the `JSONLT` object is made available globally:

```html
<script src="path/to/jsonlt.js"></script>
<script>
    const inputData = { name: "Bob" };

    const jsonltConfig = {
        transformations: [
            { type: "rename", path: ".", source: "name", target: "fullName" }
        ]
    };

    const output = JSONLT.transform(inputData, jsonltConfig);
    console.log(output);
    // Output: { fullName: 'Bob' }
</script>
```

### Demo Page

A demo HTML page is included in the `demo` folder. You can use this to test JSONLT transformations in your browser. To use the demo:

1. Build the project: `npm run build`
2. Open `demo/index.html` in your web browser

Alternatively, you can try the online demo at: https://irrelative.github.io/jsonlt/

## Development

To set up the development environment:

1. Clone the repository
2. Run `npm install` to install dependencies
3. Use `npm test` to run the test suite
4. Use `npm run build` to build the distribution file

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
