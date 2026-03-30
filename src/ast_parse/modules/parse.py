from pathlib import Path
from tree_sitter_cpp import language
from tree_sitter import Node, Language, Parser
from ast_parse.public.node_view import TsNodeView

def parse_content(content: bytes) -> TsNodeView:
    cpp_lang = Language(language())
    parser = Parser(language=cpp_lang)
    tree = parser.parse(content)
    root_node = tree.root_node
    return TsNodeView.from_node(root_node)

def parse_code_str(code_content: str) -> TsNodeView:
    return parse_content(code_content.encode(encoding="utf-8"))

def parse_code_file(file: Path):
    if not file.is_file():
        raise FileExistsError(f"file {file} must be valid file")
    with file.open("rb") as f:
        content = f.read()
        return parse_content(content=content)