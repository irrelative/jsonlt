from pydantic import BaseModel
from typing import Union, Optional, Any, Literal


class RenameTransformation(BaseModel):
    """Model for renaming keys or attributes"""

    type: Literal["rename"] = "rename"
    source: str
    target: str


class ReorderTransformation(BaseModel):
    """Model for reordering elements within an object"""

    type: Literal["reorder"] = "reorder"
    order: list[str]


class ConvertAttributeToElement(BaseModel):
    """Model for converting attributes to elements"""

    type: Literal["attribute_to_element"] = "attribute_to_element"
    source: str
    target: str


class ConvertElementToAttribute(BaseModel):
    """Model for converting elements to attributes"""

    type: Literal["element_to_attribute"] = "element_to_attribute"
    source: str
    target: str


class ConditionalTransformation(BaseModel):
    """Model for applying transformations conditionally"""

    type: Literal["conditional"] = "conditional"
    condition: str
    true_transformation: (
        "Transformation"  # Recursively reference the Transformation model
    )
    false_transformation: Optional["Transformation"] = None


class MergeTransformation(BaseModel):
    """Model for merging elements"""

    type: Literal["merge"] = "merge"
    sources: list[str]
    target: str


class SplitTransformation(BaseModel):
    """Model for splitting elements"""

    type: Literal["split"] = "split"
    source: str
    targets: list[str]


class AddElementTransformation(BaseModel):
    """Model for adding new elements or attributes"""

    type: Literal["add"] = "add"
    target: str
    value: Any


class RemoveElementTransformation(BaseModel):
    """Model for removing elements or attributes"""

    type: Literal["remove"] = "remove"
    target: str


class TextModificationTransformation(BaseModel):
    """Model for modifying text content"""

    type: Literal["modify_text"] = "modify_text"
    target: str
    modification: str


class CopyStructureTransformation(BaseModel):
    """Model for copying the entire structure with modifications"""

    type: Literal["copy_structure"] = "copy_structure"
    modifications: list["Transformation"]


class GroupTransformation(BaseModel):
    """Model for grouping elements"""

    type: Literal["group"] = "group"
    source: str
    target: str
    group_by: str


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
]


class JSONLT(BaseModel):
    """Model for the JSONLT transformation structure"""

    transformations: list[Transformation]

    class Config:
        title = "JSONLT"


if __name__ == "__main__":
    import json
    from pydantic.json_schema import model_json_schema

    json_schema = model_json_schema(JSONLT)
    print(json.dumps(json_schema, indent=2))
