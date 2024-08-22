from enum import Enum
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel


class TextModification(str, Enum):
    uppercase = "uppercase"
    lowercase = "lowercase"
    capitalize = "capitalize"
    title = "title"
    strip = "strip"
    replace = "replace"


class RenameTransformation(BaseModel):
    """Model for renaming keys or attributes"""

    type: Literal["rename"] = "rename"
    path: str = "."
    source: str
    target: str


class ReorderTransformation(BaseModel):
    """Model for reordering elements within an object"""

    type: Literal["reorder"] = "reorder"
    path: str = "."
    order: list[str]


class ConvertAttributeToElement(BaseModel):
    """Model for converting attributes to elements"""

    type: Literal["attribute_to_element"] = "attribute_to_element"
    path: str = "."
    source: str
    target: str


class ConvertElementToAttribute(BaseModel):
    """Model for converting elements to attributes"""

    type: Literal["element_to_attribute"] = "element_to_attribute"
    path: str = "."
    source: str
    target: str


class Condition(BaseModel):
    """Model for condition representation"""

    operator: Literal["eq", "ne", "gt", "lt", "ge", "le", "and", "or", "not"]
    left: Union[str, "Condition"]
    right: Optional[Union[Any, "Condition"]] = None


class ConditionalTransformation(BaseModel):
    """Model for applying transformations conditionally"""

    type: Literal["conditional"] = "conditional"
    path: str = "."
    condition: Condition
    true_transformation: (
        "Transformation"  # Recursively reference the Transformation model
    )
    false_transformation: Optional["Transformation"] = None


class MergeTransformation(BaseModel):
    """Model for merging elements"""

    type: Literal["merge"] = "merge"
    path: str = "."
    sources: list[str]
    target: str


class SplitTransformation(BaseModel):
    """Model for splitting elements"""

    type: Literal["split"] = "split"
    path: str = "."
    source: str
    targets: list[str]


class AddElementTransformation(BaseModel):
    """Model for adding new elements or attributes"""

    type: Literal["add"] = "add"
    path: str = "."
    target: str
    value: Any


class RemoveElementTransformation(BaseModel):
    """Model for removing elements or attributes"""

    type: Literal["remove"] = "remove"
    path: str = "."
    target: str


class TextModificationTransformation(BaseModel):
    """Model for modifying text content"""

    type: Literal["modify_text"] = "modify_text"
    path: str = "."
    target: str
    modification: TextModification
    replace_old: Optional[str] = None
    replace_new: Optional[str] = None


class CopyStructureTransformation(BaseModel):
    """Model for copying the entire structure with modifications"""

    type: Literal["copy_structure"] = "copy_structure"
    path: str = "."
    modifications: list["Transformation"]


class GroupTransformation(BaseModel):
    """Model for grouping elements"""

    type: Literal["group"] = "group"
    path: str = "."
    source: str
    target: str
    group_by: str


class ConcatTransformation(BaseModel):
    """Model for concatenating multiple fields"""

    type: Literal["concat"] = "concat"
    path: str = "."
    sources: list[str]
    target: str
    delimiter: Optional[str] = None


Transformation = Union[
    RenameTransformation,
    ReorderTransformation,
    ConvertAttributeToElement,
    ConvertElementToAttribute,
    ConditionalTransformation,
    MergeTransformation,
    SplitTransformation,
    AddElementTransformation,
    RemoveElementTransformation,
    TextModificationTransformation,
    CopyStructureTransformation,
    GroupTransformation,
    ConcatTransformation,
]


class JSONLT(BaseModel):
    """Model for the JSONLT transformation structure"""

    transformations: list[Transformation]

    class ConfigDict:
        title = "JSONLT"


if __name__ == "__main__":
    import json

    from pydantic.json_schema import model_json_schema

    json_schema = model_json_schema(JSONLT)
    print(json.dumps(json_schema, indent=2))
