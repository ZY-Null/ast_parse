from ast_parse.modules.parse import *
from sys import argv as input_params
from pathlib import Path
import json

def do_work():
    if len(input_params) < 2:
        return
    file = Path(input_params[1])
    target_file = Path(str(file)+".json")
    node_view = create_root_node_view(parse_code_file(file))
    with target_file.open("w", encoding="utf-8") as f:
        json.dump(node_view.model_dump(), f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    do_work()