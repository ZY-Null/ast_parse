from tree_sitter import Node
from typing import ClassVar, Callable
from ast_parse.public.byte_decode import decode_bytes

class TSNodeId:
    _cls_method_cache: ClassVar[dict[str, Callable[[Node], str]]] = {}
    
    def __init__(self, node: Node):
        self._node: Node = node
        self._node_id: str| None = None
        
    @property
    def node_id(self):
        if self._node_id is None:
            self._node_id = self.get_treesitter_node_id_entry_intf(node=self._node)
        return self._node_id

    @staticmethod
    def get_treesitter_node_id_entry_intf(node: Node) -> str:
        node_type = node.type
        if node_type not in TSNodeId._cls_method_cache:
            method_func: Callable[[Node], str] = None
            target_name = f"get_treesitter_node_id_impl_{node_type}"
            method_func = getattr(TSNodeId, target_name, None)
            TSNodeId._cls_method_cache[node_type] = method_func
        if TSNodeId._cls_method_cache[node_type] is None:
            return ""
        return TSNodeId._cls_method_cache[node_type](node)
    
    @staticmethod
    def tool_convert_treesitter_node_byte_text_to_str(node: Node)-> str:
        decode_result = decode_bytes(node.text)
        if not decode_result.encoding:
            return ""
        return decode_result.text
    
    @staticmethod
    def tool_get_treesitter_node_child_id_by_type(node: Node, type_list: list[str])->str:
        if not node.children:
            return ""
        for child in node.children:
            if child.type in type_list:
                return TSNodeId.tool_convert_treesitter_node_byte_text_to_str(node=child)
        return ""
    
    @staticmethod
    def get_treesitter_node_id_impl_preproc_include(node: Node)-> str:
        if node.type != "preproc_include":
            return ""
        child_candidates: list[str] = [
            "system_lib_string",
            "string_literal"
        ]
        raw_id = TSNodeId.tool_get_treesitter_node_child_id_by_type(node=node, type_list=child_candidates)
        node_id = raw_id.strip("\"<>")
        return node_id