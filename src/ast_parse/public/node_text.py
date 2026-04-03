from tree_sitter import Node
from typing import ClassVar, Callable
from ast_parse.public.byte_decode import decode_bytes

class TsNodeText:
    _cls_method_cache: ClassVar[dict[str, Callable[[Node], str]]] = {}

    def __init__(self, node: Node):
        self._node: Node = node
        self._node_text: str| None = None

    @property
    def text(self):
        if self._node_text is None:
            self._node_text = self.get_node_text_entry(node=self._node)
        return self._node_text

    @staticmethod
    def get_root_node(node: Node) -> Node:
        def _upswing(cur_node: Node)->Node:
            node_p = cur_node.parent
            if node_p is None:
                return cur_node
            else:
                return _upswing(cur_node=node_p)
        r_node = _upswing(cur_node=node)
        return r_node

    @staticmethod
    def get_node_text_entry(node: Node) -> str:
        return TsNodeText.__get_this_node_text_entry(node=node)

    @staticmethod
    def __get_this_node_text_entry(node: Node) -> str:
        node_type = node.type
        if node_type not in TsNodeText._cls_method_cache:
            method_func: Callable[[Node], str] = None
            target_name = f"get_treesitter_node_text_{node_type}"
            method_func = getattr(TsNodeText, target_name, None)
            TsNodeText._cls_method_cache[node_type] = method_func
        if TsNodeText._cls_method_cache[node_type] is None:
            return TsNodeText.get_node_self_text(node=node)
        return TsNodeText._cls_method_cache[node_type](node)

    @staticmethod
    def get_node_self_text(node: Node) -> str:
        return decode_bytes(node.text).text

    @staticmethod
    def get_node_self_text_with_head_comments(node: Node) -> str:
        start_byte, end_byte = node.start_byte, node.end_byte
        first_line = node.start_point.row
        big_bro = node.prev_sibling
        while big_bro:
            if big_bro.type != "comment":
                break
            cur_end_line = big_bro.end_point.row
            if first_line - 1 <= cur_end_line <= first_line:
                # 如果当前注释节点正好和前一个非注释节点同一行，最好不要获取
                big_big_bro = big_bro.prev_sibling
                if big_big_bro is not None:
                    if big_big_bro.type != "comment":
                        if big_big_bro.end_point.row == big_bro.start_point.row:
                            break
                start_byte = big_bro.start_byte
                first_line = big_bro.start_point.row
                big_bro = big_big_bro
            else:
                break
        r_node = TsNodeText.get_root_node(node=node)
        target_bytes = r_node.text[start_byte:end_byte]
        content = decode_bytes(target_bytes).text
        return content
    
    @staticmethod
    def get_node_self_text_with_post_comments(node: Node) -> str:
        start_byte, end_byte = node.start_byte, node.end_byte
        last_line = node.start_point.row
        little_bro = node.next_sibling
        while little_bro:
            if little_bro.type != "comment":
                break
            cur_first_line = little_bro.start_point.row
            if cur_first_line == last_line:
                end_byte = little_bro.end_byte
                last_line = little_bro.end_point.row
                litlittle_bro = little_bro.next_sibling
                little_bro = litlittle_bro
            else:
                break
        r_node = TsNodeText.get_root_node(node=node)
        target_bytes = r_node.text[start_byte:end_byte]
        content = decode_bytes(target_bytes).text
        return content

    @staticmethod
    def get_treesitter_node_text_function_declarator(node: Node) -> str:
        target_parent_types: list[str] = ["template_declaration"]
        node_p = node.parent
        if node_p is not None and node_p.type in target_parent_types:
            return TsNodeText.get_node_text_entry(node=node_p)
        return TsNodeText.get_node_self_text_with_head_comments(node=node)

    @staticmethod
    def get_treesitter_node_text_template_declaration(node: Node) -> str:
        return TsNodeText.get_node_self_text_with_head_comments(node=node)

