from sys import argv
from pathlib import Path
from tree_sitter_cpp import language
from tree_sitter import Node, Language, Parser
import json
from ast_parse.public.node_view import TsNodeView
from ast_parse.public.byte_decode import decode_bytes


def dump_node(cur_node: Node, level: int = 0) -> dict:
    modelObject = TsNodeView.from_node(cur_node)
    return modelObject.model_dump()


def prt_content_recurse(content:bytes, recurse_count = 0):
    res = decode_bytes(content)
    bytes_list = bytearray(content.decode(encoding=res.encoding), encoding="utf-8")
    for i  in range(len(bytes_list)):
        if i % (recurse_count % 10 + 1) == 0:
            print(bytes_list[i], end=" ")
    print()
    if recurse_count >= 500:
        return 
    prt_content_recurse(bytes(bytes_list), recurse_count+1)

def _parse_content(content: bytes) -> Node:
    cpp_lang = Language(language())
    parser = Parser(language=cpp_lang)
    tree = parser.parse(content)
    root = tree.root_node
    return root
        

def parse_cpp_file(file: Path):
    if not file.is_file():
        raise FileExistsError(f"file {file} is not valid file!")
    with file.open("rb") as f:
        content = f.read()
    root = _parse_content(content)
    return root

def main():
    for arg in argv:
        print(arg)
    print("Hello from ast-parse!")
    if len(argv) > 1:
        file = Path(argv[1])
        node = parse_cpp_file(file=file)
        with Path(str(file)+".json").open("w", encoding="utf-8") as f:
            json.dump(TsNodeView.from_node(node=node).model_dump(), f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
