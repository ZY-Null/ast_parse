from ast_parse.public import *
from tree_sitter import Tree, Node
from pathlib import Path
from typing import Callable


def collect_func_definition_from_prj(symbol: str, prj_path: Path):
    code_files: list[Path] = collect_code_files_from_prj(prj_path=prj_path)
    filtered_files: list[Path] = is_content_in_files(file_paths=code_files, search_content=symbol, whole_word=True, case_sensitive=True, is_regex=False)
    target_types: list[str] = ["function_definition"]
    target_nodes: list[TsNodeView] = [
        TsNodeView.from_node(node, with_children=False, src=str(file))
        for file in filtered_files
            for node in _get_symbol_nodes_from_file(symbol=symbol, file=file, target_node_types=target_types)
        ]
    # contents: list[str] = [n.text for n in target_nodes]
    return target_nodes

def _get_symbol_nodes_from_file(symbol: str, file: Path, target_node_types: list[str]|None = None) -> list[Node]:
    t: Tree = parse_code_file(file=file)
    root = t.root_node
    target_nodes = _find_node_by_name(symbol_name=symbol, root_node=root, target_node_types=target_node_types)
    return target_nodes

def _find_node_by_name(symbol_name: str, root_node: Node, target_node_types: list[str]|None = None)->list[Node]:
    _is_type_match = lambda t: True
    if target_node_types:
        _is_type_match = lambda t: t in target_node_types

    def _find_node_impl(target_name: list[str], cur_node: Node, type_matcher: Callable[[str], bool])->list[Node]:
        if type_matcher(cur_node.type):
            id_getter = TSNodeId(node=cur_node)
            cur_ids = id_getter.node_id_list
            match_res = match_name_list(target_name, cur_ids)
            if match_res != 0:
                return [cur_node]
        match_result: list[Node] = []
        for child in cur_node.children:
            match_result.extend(_find_node_impl(target_name=target_name, cur_node=child, type_matcher=type_matcher))
        return match_result
    
    result = _find_node_impl(target_name=symbol_name.split("::"), cur_node=root_node, type_matcher=_is_type_match)
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