import pytest
from xform import jsonlt_transform

def test_rename_transformation():
    data = {"person": {"firstName": "John", "lastName": "Doe"}}
    jsonlt_conf = {
        "transformations": [
            {"type": "rename", "source": "firstName", "target": "givenName"},
            {"type": "rename", "source": "lastName", "target": "familyName"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "givenName" in result["person"]
    assert "familyName" in result["person"]
    assert "firstName" not in result["person"]
    assert "lastName" not in result["person"]
    assert result["person"]["givenName"] == "John"
    assert result["person"]["familyName"] == "Doe"

def test_reorder_transformation():
    data = {"a": 1, "b": 2, "c": 3}
    jsonlt_conf = {
        "transformations": [
            {"type": "reorder", "order": ["c", "a", "b"]}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert list(result.keys()) == ["c", "a", "b"]

def test_attribute_to_element_transformation():
    data = {"person": {"age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "attribute_to_element", "source": "age", "target": "ageInfo"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "ageInfo" in result["person"]
    assert "age" in result["person"]["ageInfo"]
    assert result["person"]["ageInfo"]["age"] == 30

def test_element_to_attribute_transformation():
    data = {"person": {"name": {"first": "John", "last": "Doe"}}}
    jsonlt_conf = {
        "transformations": [
            {"type": "element_to_attribute", "source": "name", "target": "fullName"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "fullName" in result["person"]
    assert result["person"]["fullName"] == "John"

def test_conditional_transformation():
    data = {"person": {"age": 25}}
    jsonlt_conf = {
        "transformations": [
            {
                "type": "conditional",
                "condition": {"operator": "gt", "left": "person.age", "right": "18"},
                "true_transformation": {"type": "add", "target": "person.status", "value": "adult"},
                "false_transformation": {"type": "add", "target": "person.status", "value": "minor"}
            }
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert result["person"]["status"] == "adult"

def test_merge_transformation():
    data = {"person": {"name": {"first": "John", "last": "Doe"}, "age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "merge", "sources": ["name", "age"], "target": "info"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "info" in result["person"]
    assert "first" in result["person"]["info"]
    assert "last" in result["person"]["info"]
    assert "age" in result["person"]["info"]

def test_split_transformation():
    data = {"person": {"fullName": {"first": "John", "last": "Doe"}}}
    jsonlt_conf = {
        "transformations": [
            {"type": "split", "source": "fullName", "targets": ["firstName", "lastName"]}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "firstName" in result["person"]
    assert "lastName" in result["person"]
    assert result["person"]["firstName"] == "John"
    assert result["person"]["lastName"] == "Doe"

def test_add_element_transformation():
    data = {"person": {"name": "John Doe"}}
    jsonlt_conf = {
        "transformations": [
            {"type": "add", "target": "person.age", "value": 30}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "age" in result["person"]
    assert result["person"]["age"] == 30

def test_remove_element_transformation():
    data = {"person": {"name": "John Doe", "age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "remove", "target": "person.age"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "age" not in result["person"]

def test_modify_text_transformation():
    data = {"person": {"name": "john doe"}}
    jsonlt_conf = {
        "transformations": [
            {"type": "modify_text", "target": "person.name", "modification": "title"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert result["person"]["name"] == "John Doe"

def test_copy_structure_transformation():
    data = {"name": "John Doe", "age": 30}
    jsonlt_conf = {
        "transformations": [
            {
                "type": "copy_structure",
                "modifications": [
                    {"type": "add", "target": "occupation", "value": "Engineer"}
                ]
            }
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "occupation" in result
    assert result["occupation"] == "Engineer"

def test_group_transformation():
    data = {
        "employees": [
            {"name": "John", "department": "IT"},
            {"name": "Alice", "department": "HR"},
            {"name": "Bob", "department": "IT"}
        ]
    }
    jsonlt_conf = {
        "transformations": [
            {"type": "group", "source": "employees", "target": "grouped_employees", "group_by": "department"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "grouped_employees" in result
    assert "IT" in result["grouped_employees"]
    assert "HR" in result["grouped_employees"]
    assert len(result["grouped_employees"]["IT"]) == 2
    assert len(result["grouped_employees"]["HR"]) == 1
