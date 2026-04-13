#!/usr/bin/env python3

from ast_parse import collect_func_definition_from_prj, collect_code_element_by_pos, DumpProcess
from sys import argv as params
from pathlib import Path
import json

def print_json_dump(data):
    content = json.dumps(data, indent=4, ensure_ascii=False)
    print(content)
    return


def run_task():
    if len(params) < 2:
        raise ValueError(f"param input err, usage `{Path(__file__).name} <function_type> [args...]` to use this!")
    handles = {
        "get_symbol": get_function_by_symbol,
        "get_position": get_element_by_position,
    }
    oper_type = params[1]
    args = params[2:]
    if oper_type not in handles:
        valid_types = "\n".join(handles.keys())
        raise KeyError(f"operator type [{oper_type}] not in valid types! shown below:\n{valid_types}")
    return handles[oper_type](*args)

def get_function_by_symbol(*args):
    if len(args) < 2:
        raise ValueError(f"param input err, usage: `{Path(__file__).name} \"get_symbol\" <symbol_name> <project_path>`")
    symbol_name = args[1]
    project_path = Path(args[2])
    DumpProcess.set_process_type("DUMP")
    return collect_func_definition_from_prj(symbol=symbol_name, prj_path=project_path)

def get_element_by_position(*args):
    if len(args) < 2:
        raise ValueError(f"param input err, usage: `{Path(__file__).name} \"get_position\" <file_abs_path> <line_num>`")
    file = Path(args[0])
    line_num = int(args[1])
    DumpProcess.set_process_type("DUMP")
    return collect_code_element_by_pos(file_path=file, line_num=line_num)

if __name__ == "__main__":
    exc_result = run_task()
    print_json_dump(exc_result)
