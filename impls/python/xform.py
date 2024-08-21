# Transform json to json using jsonlt object

from schema_gen import JSONLT, Condition
from typing import Any, Dict, List, Union, Optional
import copy
import operator


def rename_transformation(data: Dict[str, Any], source: str, target: str) -> Dict[str, Any]:
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            new_data[key] = rename_transformation(value, source, target)
        elif key == source:
            new_data[target] = value
        else:
            new_data[key] = value
    return new_data


def reorder_transformation(data: Dict[str, Any], order: List[str]) -> Dict[str, Any]:
    return {key: data[key] for key in order if key in data}


def attribute_to_element_transformation(data: Dict[str, Any], source: str, target: str) -> Dict[str, Any]:
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            new_data[key] = attribute_to_element_transformation(value, source, target)
        elif key == source:
            new_data[target] = {source: value}
        else:
            new_data[key] = value
    return new_data


def element_to_attribute_transformation(data: Dict[str, Any], source: str, target: str) -> Dict[str, Any]:
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            if key == source:
                new_data[target] = next(iter(value.values()))
            else:
                new_data[key] = element_to_attribute_transformation(value, source, target)
        else:
            new_data[key] = value
    return new_data


def evaluate_condition(condition: Condition, data: Dict[str, Any]) -> bool:
    ops = {
        "eq": operator.eq,
        "ne": operator.ne,
        "gt": operator.gt,
        "lt": operator.lt,
        "ge": operator.ge,
        "le": operator.le,
        "and": lambda x, y: x and y,
        "or": lambda x, y: x or y,
        "not": lambda x: not x
    }

    def resolve_value(value: Union[str, Condition], data: Dict[str, Any]) -> Any:
        if isinstance(value, Condition):
            return evaluate_condition(value, data)
        elif isinstance(value, str):
            # Assume it's a path to a value in the data
            parts = value.split('.')
            current = data
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    try:
                        return int(value)  # Try to convert to int if it's a number
                    except ValueError:
                        return value  # If not found or not a number, treat it as a literal value
            return current
        else:
            return value

    def evaluate_condition(condition: Condition, data: Dict[str, Any]) -> bool:
        # ... (keep the existing code)
        left = resolve_value(condition.left, data)
        right = resolve_value(condition.right, data) if condition.right is not None else None
        # ... (keep the rest of the existing code)

    left = resolve_value(condition.left, data)
    right = resolve_value(condition.right, data) if condition.right is not None else None

    if condition.operator == "not":
        return ops[condition.operator](left)
    else:
        return ops[condition.operator](left, right)

def conditional_transformation(data: Dict[str, Any], condition: Condition, true_transformation: Dict[str, Any], false_transformation: Dict[str, Any] = None) -> Dict[str, Any]:
    if evaluate_condition(condition, data):
        return apply_transformation(data, true_transformation)
    elif false_transformation:
        return apply_transformation(data, false_transformation)
    return data


def merge_transformation(data: Dict[str, Any], sources: List[str], target: str) -> Dict[str, Any]:
    def merge_recursive(d: Dict[str, Any]) -> Dict[str, Any]:
        merged = {}
        new_d = {}
        for key, value in d.items():
            if key in sources:
                if isinstance(value, dict):
                    merged.update(value)
                else:
                    merged[key] = value
            else:
                if isinstance(value, dict):
                    new_d[key] = merge_recursive(value)
                else:
                    new_d[key] = value
        if merged:
            new_d[target] = merged
        return new_d
    return merge_recursive(data)


def split_transformation(data: Dict[str, Any], source: str, targets: List[str]) -> Dict[str, Any]:
    def split_recursive(d: Dict[str, Any]) -> Dict[str, Any]:
        if source in d and isinstance(d[source], dict):
            source_data = d.pop(source)
            for i, target in enumerate(targets):
                if i < len(source_data):
                    d[target] = list(source_data.values())[i]
        for key, value in d.items():
            if isinstance(value, dict):
                d[key] = split_recursive(value)
        return d
    return split_recursive(data)


def add_element_transformation(data: Dict[str, Any], target: str, value: Any) -> Dict[str, Any]:
    def add_recursive(d: Dict[str, Any], path: List[str]) -> Dict[str, Any]:
        if len(path) == 1:
            d[path[0]] = value
        elif path[0] in d:
            d[path[0]] = add_recursive(d[path[0]], path[1:])
        else:
            d[path[0]] = add_recursive({}, path[1:])
        return d
    return add_recursive(data, target.split('.'))


def remove_element_transformation(data: Dict[str, Any], target: str) -> Dict[str, Any]:
    def remove_recursive(d: Dict[str, Any], path: List[str]) -> Dict[str, Any]:
        if len(path) == 1:
            if path[0] in d:
                del d[path[0]]
        elif path[0] in d and isinstance(d[path[0]], dict):
            d[path[0]] = remove_recursive(d[path[0]], path[1:])
        return d
    return remove_recursive(data, target.split('.'))


def modify_text_transformation(data: Dict[str, Any], target: str, modification: str, replace_old: Optional[str] = None, replace_new: Optional[str] = None) -> Dict[str, Any]:
    def modify_recursive(d: Dict[str, Any], path: List[str]) -> Dict[str, Any]:
        if len(path) == 1 and path[0] in d and isinstance(d[path[0]], str):
            if modification == "uppercase":
                d[path[0]] = d[path[0]].upper()
            elif modification == "lowercase":
                d[path[0]] = d[path[0]].lower()
            elif modification == "capitalize":
                d[path[0]] = d[path[0]].capitalize()
            elif modification == "title":
                d[path[0]] = d[path[0]].title()
            elif modification == "strip":
                d[path[0]] = d[path[0]].strip()
            elif modification == "replace":
                if replace_old is not None and replace_new is not None:
                    d[path[0]] = d[path[0]].replace(replace_old, replace_new)
        elif path[0] in d and isinstance(d[path[0]], dict):
            d[path[0]] = modify_recursive(d[path[0]], path[1:])
        return d
    return modify_recursive(data, target.split('.'))


def copy_structure_transformation(data: Dict[str, Any], modifications: List[Dict[str, Any]]) -> Dict[str, Any]:
    copied_data = copy.deepcopy(data)
    for modification in modifications:
        copied_data = apply_transformation(copied_data, modification)
    return copied_data  # Return the modified copy directly


def group_transformation(data: Dict[str, Any], source: str, target: str, group_by: str) -> Dict[str, Any]:
    if source in data and isinstance(data[source], list):
        grouped = {}
        for item in data[source]:
            if group_by in item:
                key = item[group_by]
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(item)
        data[target] = grouped
        del data[source]
    return data


def apply_transformation(data: Dict[str, Any], transformation: Dict[str, Any]) -> Dict[str, Any]:
    transformation_type = transformation['type']
    if transformation_type == 'rename':
        return rename_transformation(data, transformation['source'], transformation['target'])
    elif transformation_type == 'reorder':
        return reorder_transformation(data, transformation['order'])
    elif transformation_type == 'attribute_to_element':
        return attribute_to_element_transformation(data, transformation['source'], transformation['target'])
    elif transformation_type == 'element_to_attribute':
        return element_to_attribute_transformation(data, transformation['source'], transformation['target'])
    elif transformation_type == 'conditional':
        condition = Condition(**transformation['condition'])
        return conditional_transformation(data, condition, transformation['true_transformation'], transformation.get('false_transformation'))
    elif transformation_type == 'merge':
        return merge_transformation(data, transformation['sources'], transformation['target'])
    elif transformation_type == 'split':
        return split_transformation(data, transformation['source'], transformation['targets'])
    elif transformation_type == 'add':
        return add_element_transformation(data, transformation['target'], transformation['value'])
    elif transformation_type == 'remove':
        return remove_element_transformation(data, transformation['target'])
    elif transformation_type == 'modify_text':
        return modify_text_transformation(
            data,
            transformation['target'],
            transformation['modification'],
            transformation.get('replace_old'),
            transformation.get('replace_new')
        )
    elif transformation_type == 'copy_structure':
        return copy_structure_transformation(data, transformation['modifications'])
    elif transformation_type == 'group':
        return group_transformation(data, transformation['source'], transformation['target'], transformation['group_by'])
    return data


def jsonlt_transform(json_data: Dict[str, Any], jsonlt_conf: Dict[str, Any]) -> Dict[str, Any]:
    transformed_data = copy.deepcopy(json_data)
    jsonlt = JSONLT(**jsonlt_conf)
    
    for transformation in jsonlt.transformations:
        transformed_data = apply_transformation(transformed_data, transformation.dict())
    
    return transformed_data

if __name__ == "__main__":
    # Sample JSON data
    sample_data = {
        "person": {
            "firstName": "John",
            "lastName": "Doe",
            "age": 30
        }
    }

    # Sample JSONLT configuration
    sample_jsonlt_conf = {
        "transformations": [
            {
                "type": "rename",
                "source": "firstName",
                "target": "givenName"
            },
            {
                "type": "rename",
                "source": "lastName",
                "target": "familyName"
            },
            {
                "type": "add",
                "target": "fullName",
                "value": ""
            },
            #{
            #    "type": "modify_text",
            #    "target": "fullName",
            #    "modification": "f'{data[\"person\"][\"givenName\"]} {data[\"person\"][\"familyName\"]}'"
            #}
        ]
    }

    # Perform the transformation
    result = jsonlt_transform(sample_data, sample_jsonlt_conf)

    # Print the result
    import json
    print("Original data:")
    print(json.dumps(sample_data, indent=2))
    print("\nTransformed data:")
    print(json.dumps(result, indent=2))
