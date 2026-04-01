from sys import argv
from pathlib import Path
import json
from ast_parse.modules.parse import parse_with_callback, create_read_callback, create_root_node_view

def parse_cpp_file(file: Path):
    if not file.is_file():
        raise FileExistsError(f"file {file} is not valid file!")
    with file.open("rb") as f:
        content = f.read()
    rd_cb = create_read_callback(source=content)
    t = parse_with_callback(rd_cb)
    return create_root_node_view(t)

def main():
    for arg in argv:
        print(arg)
    print("Hello from ast-parse!")
    if len(argv) > 1:
        file = Path(argv[1])
        node = parse_cpp_file(file=file)
        with Path(str(file)+".json").open("w", encoding="utf-8") as f:
            json.dump(node.model_dump(), f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
