from sys import argv
from pathlib import Path
from tree_sitter_cpp import language
from tree_sitter import Node, Language, Parser
import json
from ast_parse.public.node_view import TNodeView


def dump_node(cur_node: Node, level: int = 0) -> dict:
    modelObject = TNodeView.from_node(cur_node)
    return modelObject.model_dump()

def parse_cpp_file(file: Path):
    if not file.is_file():
        raise FileExistsError(f"file {file} is not valid file!")
    with file.open("rb") as f:
        content = f.read()
    cpp_lang = Language(language())
    parser = Parser(language=cpp_lang)
    tree = parser.parse(content)
    root = tree.root_node
    code_obj = dump_node(root)
    dump_file = file.parent / f"{file.name}.json"
    with dump_file.open("w", encoding="utf-8") as f:
        json.dump(code_obj, f, indent=4, ensure_ascii=False)

def main():
    for arg in argv:
        print(arg)
    print("Hello from ast-parse!")
    if len(argv) > 1:
        file = Path(argv[1])
        parse_cpp_file(file=file)


if __name__ == "__main__":
    main()
