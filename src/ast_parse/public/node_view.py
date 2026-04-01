from ast_parse.public.byte_decode import decode_bytes
from ast_parse.public.node_id import TSNodeId
from pydantic import BaseModel, Field, PrivateAttr, model_serializer, SerializerFunctionWrapHandler
from tree_sitter import Node

class TsNodeView(BaseModel):
    _node: Node|None = PrivateAttr(default=None)
    node_type: str = Field(..., description="node type")
    node_id: str = Field(..., description="like var name, function name, cls name etc.")
    text: str = Field(..., description="code content")
    src: str = Field(..., description="file or else")
    line : int = Field(..., description="start line")
    attrs: "NodeAttrs" = Field(default_factory=dict, description="node attrs")
    children: list["TsNodeView"] = Field(default_factory=list, description="Child Node")

    class NodeAttrs(BaseModel):
        name : str|None = Field(default=None, description="node attr: name")
        body : str|None = Field(default=None, description="node attr: body")
        condition : str|None = Field(default=None, description="node attr: condition")
        value : str|None = Field(default=None, description="node attr: value")
        left : str|None = Field(default=None, description="node attr: left")
        right : str|None = Field(default=None, description="node attr: right")
        function : str|None = Field(default=None, description="node attr: function")
        arguments : str|None = Field(default=None, description="node attr: arguments")
        declarator : str|None = Field(default=None, description="node attr: declarator")
        
        @classmethod
        def from_node(cls, node: Node)->"TsNodeView.NodeAttrs":
            attrs:dict[str,str] = {}
            cur_name_node = node.child_by_field_name("name")
            if cur_name_node is not None:
                attrs["name"] = decode_bytes(cur_name_node.text).text
            cur_body_node = node.child_by_field_name("body")
            if cur_body_node is not None:
                attrs["body"] = decode_bytes(cur_body_node.text).text
            cur_condition_node = node.child_by_field_name("condition")
            if cur_condition_node is not None:
                attrs["condition"] = decode_bytes(cur_condition_node.text).text
            cur_value_node = node.child_by_field_name("value")
            if cur_value_node is not None:
                attrs["value"] = decode_bytes(cur_value_node.text).text
            cur_left_node = node.child_by_field_name("left")
            if cur_left_node is not None:
                attrs["left"] = decode_bytes(cur_left_node.text).text
            cur_right_node = node.child_by_field_name("right")
            if cur_right_node is not None:
                attrs["right"] = decode_bytes(cur_right_node.text).text
            cur_function_node = node.child_by_field_name("function")
            if cur_function_node is not None:
                attrs["function"] = decode_bytes(cur_function_node.text).text
            cur_arguments_node = node.child_by_field_name("arguments")
            if cur_arguments_node is not None:
                attrs["arguments"] = decode_bytes(cur_arguments_node.text).text
            cur_declarator_node = node.child_by_field_name("declarator")
            if cur_declarator_node is not None:
                attrs["declarator"] = decode_bytes(cur_declarator_node.text).text
            return cls.model_validate(attrs)
        
        @model_serializer(mode='wrap')
        def serialize_exclude_falsy(self, handler: SerializerFunctionWrapHandler) -> dict:
            # 1. 先获取默认的序列化结果（这是一个有序字典）
            data = handler(self)
            
            # 2. 使用字典推导式过滤 Falsy 值
            # 逻辑：只有当 value 为 True (非 Falsy) 时，才保留该键值对
            # 注意：字典推导式会保持遍历 data.items() 的原始顺序
            return {
                key: value 
                for key, value in data.items() 
                if value
            }

    @classmethod
    def from_node(cls, node: Node, with_children: bool = True, src: str = "") -> "TsNodeView":
        assert node is not None
        decode_result = decode_bytes(node.text)
        text = ""
        if decode_result.encoding:
            text = decode_result.text

        id_getter = TSNodeId(node)
        id = id_getter.node_id
        attrs = TsNodeView.NodeAttrs.from_node(node)

        children = []
        if with_children:
            children = [cls.from_node(child) for child in node.children]
        attrs = {
            "node_type": node.type,
            "node_id": id,
            "text": text,
            "src": src,
            "attrs": attrs,
            "children": children,
            "line": node.start_point.row + 1,
        }
        return cls.model_validate(attrs)

    @model_serializer(mode='wrap')
    def serialize_exclude_falsy(self, handler: SerializerFunctionWrapHandler) -> dict:
        # 1. 先获取默认的序列化结果（这是一个有序字典）
        data = handler(self)
        
        # 2. 使用字典推导式过滤 Falsy 值
        # 逻辑：只有当 value 为 True (非 Falsy) 时，才保留该键值对
        # 注意：字典推导式会保持遍历 data.items() 的原始顺序
        return {
            key: value 
            for key, value in data.items() 
            if value
        }