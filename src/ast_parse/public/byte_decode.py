from charset_normalizer import from_bytes
from pydantic import BaseModel, Field

_ENCODING_FALLBACK_LIST = [
    'utf-8', 
    'utf-8-sig',  # 对应 "utf-8 with bom"
    'gb18030',    # 修正了 gb18306，这是正确的标准名，兼容 gbk/gb2312
    'big5',       # 繁体中文常见
    'shift_jis',  # 日文常见
    'euc-kr',     # 韩文常见
    'iso-8859-1', # 西欧常见
    'windows-1252'
]

class BytesDecode(BaseModel):
    text: str = Field(..., description="字节流解析结果")
    encoding: str = Field(..., description="字节流编码格式")

def _decode_bytes(data: bytes)->BytesDecode:
    try:
        result = from_bytes(sequences=data).best()
        if result and result.encoding and result.coherence > 0.8:
            return BytesDecode.model_validate({
                "text": str(result),
                "encoding": result.encoding
            })
    except:
        pass
    
    for code_type in _ENCODING_FALLBACK_LIST:
        try:
            text = data.decode(encoding=code_type)
            return BytesDecode.model_validate({
                "text": text,
                "encoding": code_type
            })
        except:
            pass

    FINAL_CODING = "latin-1"
    return BytesDecode.model_validate({
                "text": data.decode(encoding=FINAL_CODING),
                "encoding": FINAL_CODING
            })

def decode_bytes(data: bytes)->BytesDecode:
    try:
        return _decode_bytes(data)
    except:
        return BytesDecode.model_validate({
                "text": "",
                "encoding": ""
            })

__all__ = ["decode_bytes"]