from ast_parse.modules.parse import *
from ast_parse.public.byte_decode import decode_bytes
from ast_parse.public.node_view import TsNodeView
from tree_sitter import Tree, Node
from pathlib import Path


def collect_symbol_impl_from_prj(symbol: str, prj_path: Path):
    code_files: list[Path] = collect_code_files_from_prj(prj_path=prj_path)
    filtered_files: list[Path] = is_content_in_files(file_paths=code_files, search_content=symbol, whole_word=True, case_sensitive=True, is_regex=False)
    target_nodes: list[TsNodeView] = [
        TsNodeView.from_node(node, with_children=False, src=str(file))
        for file in filtered_files
            for node in get_symbol_nodes_from_file(symbol=symbol, file=file)
        ]
    # contents: list[str] = [n.text for n in target_nodes]
    return target_nodes

def get_symbol_nodes_from_file(symbol: str, file: Path) -> list[Node]:
    t: Tree = parse_code_file(file=file)
    root = t.root_node
    target_nodes = find_node_by_name(symbol_name=symbol, cur_node=root)
    return target_nodes

def find_node_by_name(symbol_name: str, cur_node: Node)->list[Node]:
    viewer = TsNodeView.from_node(node=cur_node, with_children=False)
    full_id = viewer.node_id.split("::")
    if all(sub_symbol in full_id for sub_symbol in symbol_name.split("::")):
        return [cur_node]

    result = []
    for child in cur_node.children:
        result.extend(find_node_by_name(symbol_name=symbol_name, cur_node=child))
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