from ast_parse.modules.code_parse import collect_symbol_impl_from_prj
from sys import argv as input_params
from pathlib import Path

def test_local():
    if len(input_params) < 3:
        return
    symbol = input_params[1]
    prj_dir = input_params[2]
    result = collect_symbol_impl_from_prj(symbol=symbol, prj_path=Path(prj_dir))
    for res in result:
        print(f"{res.src}:{res.line}")
        print(res.node_type)
        print(res.text)
        print()


if __name__ == "__main__":
    test_local()