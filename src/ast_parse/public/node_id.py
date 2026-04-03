from tree_sitter import Node
from typing import ClassVar, Callable
from ast_parse.public.byte_decode import decode_bytes
import copy

def match_name_list(name1: list[str], name2: list[str]) -> int:
    # 1. 检查空列表情况
    if not name1 or not name2:
        return 0
    
    # 2. 检查最后一个元素
    if name1[-1] != name2[-1]:
        return 0
    
    match_point = 1
    l2_pivot = len(name2) - 2
    for l1_pivot in range((len(name1) - 1), -1, -1):
        if l2_pivot < 0:
            break
        t_value = name1[l1_pivot]
        l2_cursor = l2_pivot
        for l2_index in range(l2_cursor, -1, -1):
            if name2[l2_index] != t_value:
                continue
            match_point += 1
            l2_pivot = l2_index - 1
            break
    return match_point


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
        return "::".join(self._node_ids)
    
    @property
    def node_id_list(self):
        if self._node_ids is None:
            self._node_ids = self.get_treesitter_node_id_entry_intf(node=self._node)
        return copy.deepcopy(self._node_ids)
    
    @staticmethod
    def lookup_node_namespace_ids(cur_node: Node|None) -> list[str]:
        target_node_types = [
            "namespace_definition",
            "class_specifier",
            "struct_specifier",
            "union_specifier",
            "enum_specifier",
            "function_definition",
        ]
        if cur_node is None:
            return []
        cur_name = None
        if cur_node.type in target_node_types:
            name_node = cur_node.child_by_field_name("name")
            if name_node is not None:
                cur_name = TSNodeId.tool_convert_treesitter_node_byte_text_to_str(name_node)
        upper_names = TSNodeId.lookup_node_namespace_ids(cur_node=cur_node.parent)
        if cur_name is not None:
            upper_names.append(cur_name)
        return upper_names

    @staticmethod
    def __get_this_node_id_entry(node: Node) -> list[str]:
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
    def get_treesitter_node_id_entry_intf(node: Node) -> list[str]:
        self_names = TSNodeId.__get_this_node_id_entry(node=node)
        if not self_names:
            return self_names
        up_names = TSNodeId.lookup_node_namespace_ids(cur_node=node.parent)
        names = up_names + self_names
        return names
    
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
    def get_child_node_id_by_type(node: Node, target_type: str, recurse: bool = False) -> list[str]:
        if recurse:
            def _get_child_node_type_recurse(cur_node: Node, child_type: str) -> Node:
                for child in cur_node.children:
                    if child.type == child_type:
                        return child
                    else:
                        child_get = _get_child_node_type_recurse(cur_node=child, child_type=child_type)
                        if child_get is None:
                            continue
                        return child_get
                return None
            target_node = _get_child_node_type_recurse(cur_node=node, child_type=target_type)
            if target_node is None:
                return []
            return TSNodeId.__get_this_node_id_entry(target_node)
        else:
            for child in node.children:
                if child.type != target_type:
                    continue
                return TSNodeId.__get_this_node_id_entry(child)
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

    @staticmethod
    def get_treesitter_node_id_impl_function_definition(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_child_node_id_by_type(node=node, target_type="function_declarator", recurse=True)

    @staticmethod
    def get_treesitter_node_id_impl_class_specifier(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.__get_child_node_id_filter_by_type(node=node, container=TSNodeId._cls_decl_method_cache, prefix="get_node_id_")

    @staticmethod
    def get_treesitter_node_id_impl_struct_specifier(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.__get_child_node_id_filter_by_type(node=node, container=TSNodeId._cls_decl_method_cache, prefix="get_node_id_")

    @staticmethod
    def get_node_id_type_identifier(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.tool_convert_treesitter_node_byte_text_to_str(node=node).split(sep="::")

    @staticmethod
    def get_treesitter_node_id_impl_field_declaration(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.get_child_node_id_by_type(node=node, target_type="field_identifier")

    @staticmethod
    def get_treesitter_node_id_impl_field_identifier(node: Node)->list[str]:
        """ make child node can get id too """
        return TSNodeId.tool_convert_treesitter_node_byte_text_to_str(node=node).split(sep="::")