from typing import Callable, Any, Literal, ClassVar
from functools import wraps
from pydantic import BaseModel


class DumpProcess:

    _PROCESS_TYPE = Literal["ORIGIN", "DUMP"]

    _process_type : ClassVar[_PROCESS_TYPE] = "ORIGIN"
    
    @staticmethod
    def set_process_type(new_type: _PROCESS_TYPE):
        DumpProcess._process_type = new_type
    
    @staticmethod
    def get_process_type()-> _PROCESS_TYPE:
        return DumpProcess._process_type

    @staticmethod
    def _process_value(value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump()
        if isinstance(value, (int, str, float, bool, type(None))):
            return value
        if isinstance(value, list):
            return [DumpProcess._process_value(item) for item in value]
        if isinstance(value, dict):
            return {k: DumpProcess._process_value(v) for k, v in value.items()}
        if isinstance(value, tuple):
            return tuple(DumpProcess._process_value(item) for item in value)
        if isinstance(value, set):
            return {DumpProcess._process_value(item) for item in value}
        raise TypeError(f"Unsupported return type detected: {type(value)}. "
                        f"Only BaseModel, built-in types, and containers of these are allowed.")


    @staticmethod
    def ret_value_dumper(func):
        @wraps(func)
        def wrapper(*k, **kk):
            result = func(*k, **kk)
            if DumpProcess.get_process_type() == "DUMP":
                real_result = DumpProcess._process_value(result)
                return real_result
            return result
        
        return wrapper


__all__ = ["DumpProcess"]