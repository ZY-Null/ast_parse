from ast_parse.modules.parse import parse_code_file, TsNodeView
from pathlib import Path
import json

def do_parse():
    file = Path(__file__).parent / Path("script/test_code.cpp")
    return parse_code_file(file)

def collect_certain_type(cur_node: TsNodeView, target_type: str, level: int = 0):
    result = []
    if cur_node.node_type == target_type:
        result.append(cur_node)
    for child in cur_node.children:
        result.extend(collect_certain_type(child, target_type=target_type, level=level+1))
    return result

def copy_subnode_level(src_node:TsNodeView, level: int = 0) -> TsNodeView:
    src_data = {k:v for k,v in src_node.model_dump().items() if k != "children"}
    if level < 3:
        src_data["children"] = [copy_subnode_level(child, level+1) for child in src_node.children]
    return TsNodeView.model_validate(src_data)
    

def do_work():
    root = do_parse()
    nodes = collect_certain_type(root, "declaration")
    new_nodes = [copy_subnode_level(node) for node in nodes]
    datas = [node.model_dump() for node in new_nodes]
    target_file = Path(__file__).parent / Path("script/type_collect.json")
    with target_file.open("w", encoding="utf-8") as f:
        json.dump(datas, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    do_work()