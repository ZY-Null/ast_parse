from tree_sitter import Node
from typing import ClassVar, Callable
from ast_parse.public.byte_decode import decode_bytes

class TSNodeId:
    _cls_method_cache: ClassVar[dict[str, Callable[[Node], str]]] = {}
    _cls_decl_method_cache: ClassVar[dict[str, Callable[[Node], str]]] = {}
    
    def __init__(self, node: Node):
        self._node: Node = node
        self._node_ids: list[str]| None = None
        
    @property
    def node_id(self):
        if self._node_ids is None:
            self._node_ids = self.get_treesitter_node_id_entry_intf(node=self._node)
        if not self._node_ids:
            return ""
        else:
            return self._node_ids[-1]

    @staticmethod
    def get_treesitter_node_id_entry_intf(node: Node) -> list[str]:
        node_type = node.type
        if node_type not in TSNodeId._cls_method_cache:
            method_func: Callable[[Node], str] = None
            target_name = f"get_treesitter_node_id_impl_{node_type}"
            method_func = getattr(TSNodeId, target_name, None)
            TSNodeId._cls_method_cache[node_type] = method_func
        if TSNodeId._cls_method_cache[node_type] is None:
            return []
        return TSNodeId._cls_method_cache[node_type](node)
    
    @staticmethod
    def tool_convert_treesitter_node_byte_text_to_str(node: Node)-> str:
        decode_result = decode_bytes(node.text)
        if not decode_result.encoding:
            return ""
        return decode_result.text
    
    @staticmethod
    def tool_get_treesitter_node_child_id_by_type(node: Node, type_list: list[str])->list[str]:
        if not node.children:
            return []
        for child in node.children:
            if child.type in type_list:
                return TSNodeId.tool_convert_treesitter_node_byte_text_to_str(node=child)
        return []
    
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
        return [node_id]

    @staticmethod
    def __get_child_node_id_filter_by_type(node: Node, container:dict[str, Callable[[Node], str]], prefix: str = "", suffix: str ="")-> list[str]:
        for child in node.children:
            node_type = child.type
            if node_type not in container:
                method_func: Callable[[Node], str] = None
                target_name = f"{prefix}{node_type}{suffix}"
                method_func = getattr(TSNodeId, target_name, None)
                container[node_type] = method_func
            if container[node_type] is None:
                continue
            return container[node_type](child)
        return []
        

    @staticmethod
    def get_treesitter_node_id_impl_declaration(node: Node)-> list[str]:
        node_id = TSNodeId.__get_child_node_id_filter_by_type(node=node, container=TSNodeId._cls_decl_method_cache, prefix="get_node_id_")
        return node_id

    @staticmethod
    def get_node_id_init_declarator(node: Node)->list[str]:
        node_id = TSNodeId.__get_child_node_id_filter_by_type(node=node, container=TSNodeId._cls_decl_method_cache, prefix="get_node_id_")
        return node_id

    @staticmethod
    def get_node_id_function_declarator(node: Node)->list[str]:
        node_id = TSNodeId.__get_child_node_id_filter_by_type(node=node, container=TSNodeId._cls_decl_method_cache, prefix="get_node_id_")
        return node_id

    @staticmethod
    def get_node_id_pointer_declarator(node: Node)->list[str]:
        node_id = TSNodeId.__get_child_node_id_filter_by_type(node=node, container=TSNodeId._cls_decl_method_cache, prefix="get_node_id_")
        return node_id

    @staticmethod
    def get_node_id_identifier(node: Node)->list[str]:
        return TSNodeId.tool_convert_treesitter_node_byte_text_to_str(node=node).split(sep="::")

    @staticmethod
    def get_node_id_qualified_identifier(node: Node)->list[str]:
        return TSNodeId.tool_convert_treesitter_node_byte_text_to_str(node=node).split(sep="::")

    @staticmethod
    def get_treesitter_node_id_impl_init_declarator(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_node_id_init_declarator(node=node)
    @staticmethod
    def get_treesitter_node_id_impl_function_declarator(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_node_id_function_declarator(node=node)
    @staticmethod
    def get_treesitter_node_id_impl_pointer_declarator(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_node_id_pointer_declarator(node=node)
    @staticmethod
    def get_treesitter_node_id_impl_identifier(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_node_id_identifier(node=node)
    @staticmethod
    def get_treesitter_node_id_impl_qualified_identifier(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_node_id_qualified_identifier(node=node)
