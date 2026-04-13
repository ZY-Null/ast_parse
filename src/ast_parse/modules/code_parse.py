from ast_parse.public import *
from tree_sitter import Tree, Node
from pathlib import Path
from typing import Callable
from dataclasses import dataclass

@dataclass
class NodeWithHight:
    node: Node
    hight: int

def collect_functions_def_from_prj(symbols: list[str], prj_path: Path)->list[TsNodeView]:
    filtered_files: list[Path] = [prj_path]
    if prj_path.is_dir():
        code_files: list[Path] = collect_code_files_from_prj(prj_path=prj_path)
        filtered_files = is_contents_in_files(file_paths=code_files, search_contents=symbols, whole_word=True, case_sensitive=True, is_regex=False)
    target_types: list[str] = ["function_definition"]
    target_nodes: list[TsNodeView] = [
        TsNodeView.from_node(node, with_children=False, src=str(file))
        for file in filtered_files
            for node in _get_symbol_nodes_from_file(symbols=symbols, file=file, target_node_types=target_types)
        ]
    return target_nodes

@DumpProcess.ret_value_dumper
def collect_func_definition_from_prj(symbol: str, prj_path: Path):
    return collect_functions_def_from_prj(symbols=[symbol], prj_path=prj_path)

@DumpProcess.ret_value_dumper
def collect_code_element_by_pos(file_path: Path, line_num: int):
    nodes_info: list[NodeWithHight] = _collect_nodes_by_position(file=file_path, line_num=line_num)
    nodes_info.sort(key=lambda n: n.hight)
    leaf_nodes = [n.node for n in nodes_info if n.hight == 0]
    nodes_no_filtered = [get_node_global_parent_node(n) for n in leaf_nodes]
    nodes = []
    for n in nodes_no_filtered:
        if n not in nodes:
            nodes.append(n)
    node_view = [TsNodeView.from_node(node=n, with_children=False, src=str(file_path)) for n in nodes]
    return node_view

@DumpProcess.ret_value_dumper
def get_function_called_by_target_symbol(symbol: str, prj_path: Path):
    func_impl_views: list[TsNodeView] = collect_functions_def_from_prj(symbols=[symbol], prj_path=prj_path)
    func_nodes: list[Node] = [view._node for view in func_impl_views]
    return []


def get_node_global_parent_node(node: Node) -> Node:
    """ get the parent node which is exists in the global field, link function def, global val declaration, etc """
    target_node = node
    cur_node = node
    while cur_node.parent is not None:
        cur_node = cur_node.parent
        if is_global_node_type(cur_node):
            target_node = cur_node
    return target_node

def is_global_node_type(node: Node) -> bool:
    valid_types: list[str] = [
        "preproc_include", # include something
        "using_declaration", # using namespace, using something
        "template_declaration",
        "alias_declaration", # using something = something
        "type_definition",
        "declaration",
        "preproc_def",
        "preproc_function_def",
        "function_definition",
        "class_specifier",
    ]
    return node.type in valid_types
    

def _get_symbol_nodes_from_file(symbols: list[str], file: Path, target_node_types: list[str]|None = None) -> list[Node]:
    t: Tree = parse_code_file(file=file)
    root = t.root_node
    target_nodes = _find_node_by_name(symbol_names=symbols, root_node=root, target_node_types=target_node_types)
    return target_nodes

def _find_node_by_name(symbol_names: list[str], root_node: Node, target_node_types: list[str]|None = None)->list[Node]:
    _is_type_match = lambda t: True
    if target_node_types:
        _is_type_match = lambda t: t in target_node_types

    def _find_node_impl(target_names: list[list[str]], cur_node: Node, type_matcher: Callable[[str], bool])->list[Node]:
        if type_matcher(cur_node.type):
            id_getter = TSNodeId(node=cur_node)
            cur_ids = id_getter.node_id_list
            match_results = [match_name_list(target_name, cur_ids) for target_name in target_names]
            if any(res !=0 for res in match_result):
                return [cur_node]
        match_result: list[Node] = []
        for child in cur_node.children:
            match_result.extend(_find_node_impl(target_names=target_names, cur_node=child, type_matcher=type_matcher))
        return match_result
    
    result = _find_node_impl(target_name=[symbol_name.split("::") for symbol_name in symbol_names], cur_node=root_node, type_matcher=_is_type_match)
    return result


def collect_code_files_from_prj(prj_path: Path) -> list[Path]:
    files: list[Path] = []
    if not prj_path.is_dir():
        return files
    for sub_path in prj_path.iterdir():
        if sub_path.is_file():
            if is_cpp_code_file(sub_path):
                files.append(sub_path)
        elif sub_path.is_dir():
            files.extend(collect_code_files_from_prj(sub_path))
    return files

def _collect_nodes_by_position(file: Path, line_num: int, column_num: int|None = None)->list[NodeWithHight]:
    def _collect_node_by_condition(cur_node: Node, condition: Callable[[Node], bool])->tuple[int,list[NodeWithHight]]:
        result: list[NodeWithHight] = []
        child_result: list[NodeWithHight] = []
        child_hight = 0
        for child in cur_node.children:
            cur_level, cur_res = _collect_node_by_condition(cur_node=child, condition=condition)
            child_result.extend(cur_res)
            if cur_level > child_hight:
                child_hight = cur_level
        if_match = condition(cur_node)
        if if_match:
            result.append(NodeWithHight(node=cur_node, hight=child_hight))
        result.extend(child_result)
        return (child_hight + 1), result

    tree = parse_code_file(file=file)
    root = tree.root_node
    
    def _node_contains_position(cur_node: Node) -> bool:
        row_start = cur_node.start_point.row + 1
        row_end = cur_node.end_point.row + 1
        col_start = cur_node.start_point.column + 1
        col_end = cur_node.end_point.column + 1
        if row_start > line_num or row_end < line_num:
            return False
        if column_num is None:
            return True
        if line_num == row_start and column_num < col_start:
            return False
        if line_num == row_end and column_num >= col_end:
            return False
        return True

    _, result = _collect_node_by_condition(cur_node=root, condition=_node_contains_position)
    return result