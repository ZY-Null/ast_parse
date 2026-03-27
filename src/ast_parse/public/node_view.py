from ast_parse.public.byte_decode import decode_bytes
from ast_parse.public.node_id import TSNodeId
from pydantic import BaseModel, Field, PrivateAttr, computed_field
from tree_sitter import Node

class TNodeView(BaseModel):
    _node: Node|None = PrivateAttr(default=None)
    node_type: str = Field(..., description="node type")
    node_id: str = Field(..., description="like var name, function name, cls name etc.")
    text: str = Field(..., description="code content")
    children: list["TNodeView"] = Field(default_factory=list, description="Child Node")
    
    @classmethod
    def from_node(cls, node: Node) -> "TNodeView":
        assert node is not None
        decode_result = decode_bytes(node.text)
        text = ""
        if decode_result.encoding:
            text = decode_result.text
        
        id_getter = TSNodeId(node)
        id = id_getter.node_id

        children = [cls.from_node(child) for child in node.children]
        attrs = {
            "node_type": node.type,
            "node_id": id,
            "text": text,
            "children": children
        }
        return cls.model_validate(attrs)