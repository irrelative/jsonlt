from xform import jsonlt_transform

def test_rename_transformation():
    data = {"person": {"firstName": "John", "lastName": "Doe"}}
    jsonlt_conf = {
        "transformations": [
            {"type": "rename", "path": ".person", "source": "firstName", "target": "givenName"},
            {"type": "rename", "path": ".person", "source": "lastName", "target": "familyName"}
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
            {"type": "reorder", "path": ".", "order": ["c", "a", "b"]}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert list(result.keys()) == ["c", "a", "b"]

def test_attribute_to_element_transformation():
    data = {"person": {"age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "attribute_to_element", "path": ".person", "source": "age", "target": "ageInfo"}
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
            {"type": "element_to_attribute", "path": ".person", "source": "name", "target": "fullName"}
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
                "path": ".person",
                "condition": {"operator": "gt", "left": "age", "right": "18"},
                "true_transformation": {"type": "add", "path": ".", "target": "status", "value": "adult"},
                "false_transformation": {"type": "add", "path": ".", "target": "status", "value": "minor"}
            }
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert result["person"]["status"] == "adult"

def test_merge_transformation():
    data = {"person": {"name": {"first": "John", "last": "Doe"}, "age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "merge", "path": ".person", "sources": ["name", "age"], "target": "info"}
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
            {"type": "split", "path": ".person", "source": "fullName", "targets": ["firstName", "lastName"]}
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
            {"type": "add", "path": ".person", "target": "age", "value": 30}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "age" in result["person"]
    assert result["person"]["age"] == 30

def test_remove_element_transformation():
    data = {"person": {"name": "John Doe", "age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "remove", "path": ".person", "target": "age"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "age" not in result["person"]

def test_modify_text_transformation():
    data = {
        "person": {
            "name": "john doe",
            "description": "  software engineer  ",
            "email": "john.doe@example.com"
        }
    }
    jsonlt_conf = {
        "transformations": [
            {"type": "modify_text", "path": ".person", "target": "name", "modification": "title"},
            {"type": "modify_text", "path": ".person", "target": "description", "modification": "strip"},
            {"type": "modify_text", "path": ".person", "target": "email", "modification": "replace", "replace_old": "@example.com", "replace_new": "@company.com"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert result["person"]["name"] == "John Doe"
    assert result["person"]["description"] == "software engineer"
    assert result["person"]["email"] == "john.doe@company.com"

def test_copy_structure_transformation():
    data = {"name": "John Doe", "age": 30}
    jsonlt_conf = {
        "transformations": [
            {
                "type": "copy_structure",
                "path": ".",
                "modifications": [
                    {"type": "add", "path": ".", "target": "occupation", "value": "Engineer"}
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
            {"type": "group", "path": ".", "source": "employees", "target": "grouped_employees", "group_by": "department"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "grouped_employees" in result
    assert "IT" in result["grouped_employees"]
    assert "HR" in result["grouped_employees"]
    assert len(result["grouped_employees"]["IT"]) == 2
    assert len(result["grouped_employees"]["HR"]) == 1

def test_apply_path_root():
    data = {"name": "John", "age": 30}
    jsonlt_conf = {
        "transformations": [
            {"type": "add", "path": ".", "target": "occupation", "value": "Engineer"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "occupation" in result
    assert result["occupation"] == "Engineer"

def test_apply_path_nested():
    data = {"person": {"name": "John", "age": 30}}
    jsonlt_conf = {
        "transformations": [
            {"type": "add", "path": ".person", "target": "occupation", "value": "Engineer"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "occupation" in result["person"]
    assert result["person"]["occupation"] == "Engineer"

def test_apply_path_array():
    data = {"people": [{"name": "John"}, {"name": "Alice"}]}
    jsonlt_conf = {
        "transformations": [
            {"type": "add", "path": ".people[]", "target": "age", "value": 30}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert all("age" in person for person in result["people"])
    assert all(person["age"] == 30 for person in result["people"])

def test_apply_path_array_index():
    data = {"people": [{"name": "John"}, {"name": "Alice"}]}
    jsonlt_conf = {
        "transformations": [
            {"type": "add", "path": ".people[0]", "target": "age", "value": 30}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "age" in result["people"][0]
    assert result["people"][0]["age"] == 30
    assert "age" not in result["people"][1]

def test_apply_path_deep_nested():
    data = {"company": {"departments": {"IT": {"employees": [{"name": "John"}]}}}}
    jsonlt_conf = {
        "transformations": [
            {"type": "add", "path": ".company.departments.IT.employees[]", "target": "role", "value": "Developer"}
        ]
    }
    result = jsonlt_transform(data, jsonlt_conf)
    assert "role" in result["company"]["departments"]["IT"]["employees"][0]
    assert result["company"]["departments"]["IT"]["employees"][0]["role"] == "Developer"
