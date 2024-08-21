from pydantic import BaseModel, Field
from typing import Union, List, Optional, Any

class RenameTransformation(BaseModel):
    """Model for renaming keys or attributes"""
    type: str = Field("rename", const=True)
    source: str
    target: str

class ReorderTransformation(BaseModel):
    """Model for reordering elements within an object"""
    type: str = Field("reorder", const=True)
    order: List[str]

class ConvertAttributeToElement(BaseModel):
    """Model for converting attributes to elements"""
    type: str = Field("attribute_to_element", const=True)
    source: str
    target: str

class ConvertElementToAttribute(BaseModel):
    """Model for converting elements to attributes"""
    type: str = Field("element_to_attribute", const=True)
    source: str
    target: str

class ConditionalTransformation(BaseModel):
    """Model for applying transformations conditionally"""
    type: str = Field("conditional", const=True)
    condition: str
    true_transformation: 'Transformation'  # Recursively reference the Transformation model
    false_transformation: Optional['Transformation'] = None

class MergeTransformation(BaseModel):
    """Model for merging elements"""
    type: str = Field("merge", const=True)
    sources: List[str]
    target: str

class SplitTransformation(BaseModel):
    """Model for splitting elements"""
    type: str = Field("split", const=True)
    source: str
    targets: List[str]

class AddElementTransformation(BaseModel):
    """Model for adding new elements or attributes"""
    type: str = Field("add", const=True)
    target: str
    value: Any

class RemoveElementTransformation(BaseModel):
    """Model for removing elements or attributes"""
    type: str = Field("remove", const=True)
    target: str

class TextModificationTransformation(BaseModel):
    """Model for modifying text content"""
    type: str = Field("modify_text", const=True)
    target: str
    modification: str

class CopyStructureTransformation(BaseModel):
    """Model for copying the entire structure with modifications"""
    type: str = Field("copy_structure", const=True)
    modifications: List['Transformation']

class GroupTransformation(BaseModel):
    """Model for grouping elements"""
    type: str = Field("group", const=True)
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
    transformations: List[Transformation]

    class Config:
        title = "JSONLT"


if __name__ == "__main__":
    from pydantic.schema import schema
    json_schema = schema([JSONLT])
