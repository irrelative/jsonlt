# Transform json to json using jsonlt object

from schema_gen import JSONLT, Condition
from typing import Any, Dict, List, Union, Optional, Callable
import copy
import operator
from functools import reduce


def rename_transformation(data: Dict[str, Any], source: str, target: str) -> Dict[str, Any]:
    if source in data:
        data[target] = data.pop(source)
    return data


def reorder_transformation(data: Dict[str, Any], order: List[str]) -> Dict[str, Any]:
    return {key: data[key] for key in order if key in data}


def attribute_to_element_transformation(data: Dict[str, Any], source: str, target: str) -> Dict[str, Any]:
    if source in data:
        data[target] = {source: data.pop(source)}
    return data


def element_to_attribute_transformation(data: Dict[str, Any], source: str, target: str) -> Dict[str, Any]:
    if source in data and isinstance(data[source], dict):
        data[target] = next(iter(data[source].values()))
        del data[source]
    return data


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
    data[target] = value
    return data


def remove_element_transformation(data: Dict[str, Any], target: str) -> Dict[str, Any]:
    if target in data:
        del data[target]
    return data


def modify_text_transformation(data: Dict[str, Any], target: str, modification: str, replace_old: Optional[str] = None, replace_new: Optional[str] = None) -> Dict[str, Any]:
    if target in data and isinstance(data[target], str):
        if modification == "uppercase":
            data[target] = data[target].upper()
        elif modification == "lowercase":
            data[target] = data[target].lower()
        elif modification == "capitalize":
            data[target] = data[target].capitalize()
        elif modification == "title":
            data[target] = data[target].title()
        elif modification == "strip":
            data[target] = data[target].strip()
        elif modification == "replace":
            if replace_old is not None and replace_new is not None:
                data[target] = data[target].replace(replace_old, replace_new)
    return data


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

def apply_path(data: Dict[str, Any], path: str, transformation_func: Callable) -> Dict[str, Any]:
    if path == ".":
        return transformation_func(data)
    
    parts = path.split(".")
    current = data
    for i, part in enumerate(parts[1:]):  # Skip the first empty part
        if part.endswith("[]"):
            key = part[:-2]
            if key in current and isinstance(current[key], list):
                current[key] = [transformation_func(item) for item in current[key]]
            return data
        elif part.endswith("]"):
            key, index = part[:-1].split("[")
            index = int(index)
            if key in current and isinstance(current[key], list) and 0 <= index < len(current[key]):
                current[key][index] = transformation_func(current[key][index])
            return data
        elif i == len(parts) - 2:  # Last part
            if part in current:
                current[part] = transformation_func(current[part])
            return data
        else:
            if part not in current:
                current[part] = {}
            current = current[part]
    
    return data


def apply_transformation(data: Dict[str, Any], transformation: Dict[str, Any]) -> Dict[str, Any]:
    transformation_type = transformation['type']
    path = transformation.get('path', '.')

    if transformation_type == 'rename':
        return apply_path(data, path, lambda x: rename_transformation(x, transformation['source'], transformation['target']))
    elif transformation_type == 'reorder':
        return apply_path(data, path, lambda x: reorder_transformation(x, transformation['order']))
    elif transformation_type == 'attribute_to_element':
        return apply_path(data, path, lambda x: attribute_to_element_transformation(x, transformation['source'], transformation['target']))
    elif transformation_type == 'element_to_attribute':
        return apply_path(data, path, lambda x: element_to_attribute_transformation(x, transformation['source'], transformation['target']))
    elif transformation_type == 'conditional':
        condition = Condition(**transformation['condition'])
        return apply_path(data, path, lambda x: conditional_transformation(x, condition, transformation['true_transformation'], transformation.get('false_transformation')))
    elif transformation_type == 'merge':
        return apply_path(data, path, lambda x: merge_transformation(x, transformation['sources'], transformation['target']))
    elif transformation_type == 'split':
        return apply_path(data, path, lambda x: split_transformation(x, transformation['source'], transformation['targets']))
    elif transformation_type == 'add':
        return apply_path(data, path, lambda x: add_element_transformation(x, transformation['target'], transformation['value']))
    elif transformation_type == 'remove':
        return apply_path(data, path, lambda x: remove_element_transformation(x, transformation['target']))
    elif transformation_type == 'modify_text':
        return apply_path(data, path, lambda x: modify_text_transformation(
            x,
            transformation['target'],
            transformation['modification'],
            transformation.get('replace_old'),
            transformation.get('replace_new')
        ))
    elif transformation_type == 'copy_structure':
        return apply_path(data, path, lambda x: copy_structure_transformation(x, transformation['modifications']))
    elif transformation_type == 'group':
        return apply_path(data, path, lambda x: group_transformation(x, transformation['source'], transformation['target'], transformation['group_by']))
    return data


def jsonlt_transform(json_data: Dict[str, Any], jsonlt_conf: Dict[str, Any]) -> Dict[str, Any]:
    transformed_data = copy.deepcopy(json_data)
    jsonlt = JSONLT(**jsonlt_conf)
    
    for transformation in jsonlt.transformations:
        transformed_data = apply_transformation(transformed_data, transformation.dict())
    
    return transformed_data
