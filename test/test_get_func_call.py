from ast_parse.modules.code_parse import get_function_called_by_target_symbol
from ast_parse import DumpProcess
from sys import argv as input_params
from pathlib import Path
import json

def test_local():
    if len(input_params) < 3:
        return
    symbol = input_params[1]
    prj_dir = input_params[2]
    DumpProcess.set_process_type("DUMP")
    result = get_function_called_by_target_symbol(symbol=symbol, prj_path=Path(prj_dir))
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test_local()