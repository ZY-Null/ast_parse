from pathlib import Path
from tree_sitter_cpp import language
from tree_sitter import Tree, Language, Parser
from ast_parse.public.node_view import TsNodeView
from typing import Callable, Tuple, Union, List
import re

__all__ = [
    "create_root_node_view",
    "parse_with_callback",
    "parse_content",
    "parse_code_str",
    "parse_code_file",
    "is_cpp_code_file",
    "create_read_callback",
    "is_content_in_file",
    "is_content_in_files",
    "is_contents_in_files",
]

def create_root_node_view(tree: Tree) -> TsNodeView:
    root = tree.root_node
    return TsNodeView.from_node(root)

def parse_with_callback(callback: Callable[[int, Tuple[int, int]], bytes]) -> Tree:
    cpp_lang = Language(language())
    parser = Parser(language=cpp_lang)
    tree = parser.parse(callback)
    return tree

def parse_content(content: bytes) -> Tree:
    cpp_lang = Language(language())
    parser = Parser(language=cpp_lang)
    tree = parser.parse(content)
    return tree

def parse_code_str(code_content: str) -> Tree:
    return parse_content(code_content.encode(encoding="utf-8"))

def parse_code_file(file: Path) -> Tree:
    if not file.is_file():
        raise FileExistsError(f"file {file} must be valid file")
    with file.open("rb") as f:
        content = f.read()
        return parse_content(content=content)

def is_cpp_code_file(file: Path) -> bool:
    cpp_suffixes = [".c", ".C", ".cc", ".cpp", ".cxx", ".c++", ".h", ".hpp", ".hxx", ".hh",]
    return file.suffix in cpp_suffixes


# 类型定义
ReadCallback = Callable[[int, Tuple[int, int]], bytes]
DataSource = Union[bytes, bytearray, str]

def create_read_callback(
    source: DataSource, 
    encoding: str = 'utf-8',
    chunk_size: int = None
) -> ReadCallback:
    """
    创建一个优化的 Tree-sitter 读取回调函数。
    
    参数:
        source: 数据源。可以是 bytes, bytearray 或 str。
                如果是 bytearray，支持动态追加（流式场景）。
        encoding: 如果 source 是 str，使用的编码格式。
        chunk_size: 
            - 对于 bytes: 忽略此参数（为了性能，建议一次性加载）。
            - 对于 bytearray (流式): 限制单次最大返回长度（模拟网络包大小，默认为 None 即不限制）。
    
    返回:
        ReadCallback: 符合 tree-sitter 规范的回调函数。
    """
    
    # 1. 数据预处理：统一转换为 bytes 或 bytearray
    data_bytes = None
    data_mutable = None
    
    if isinstance(source, str):
        data_bytes = source.encode(encoding)
    elif isinstance(source, bytes):
        data_bytes = source
    elif isinstance(source, bytearray):
        data_mutable = source
    else:
        raise TypeError("source 必须是 bytes, bytearray 或 str")

    # 2. 定义回调逻辑
    def _read_from_immutable(offset: int, point: Tuple[int, int]) -> bytes:
        """处理不可变数据 (bytes) - 本地文件场景"""
        if offset >= len(data_bytes):
            return b""
        # 直接返回切片。Python 的 bytes 切片很快，且 Tree-sitter 会复制它需要的部分。
        # 我们不在此处人为限制步长，以避免过多的函数调用开销。
        return data_bytes[offset:]

    def _read_from_mutable(offset: int, point: Tuple[int, int]) -> bytes:
        """处理可变数据 (bytearray) - 网络流式场景"""
        if offset >= len(data_mutable):
            return b""
        
        # 流式场景：可以选择限制单次返回大小（模拟分块），也可以直接返回剩余所有
        # 通常建议直接返回剩余所有，让解析器决定读多少
        end = len(data_mutable)
        if chunk_size is not None:
            end = min(offset + chunk_size, len(data_mutable))
            
        # 返回切片（注意：bytearray 切片返回的是 bytes，符合要求）
        return data_mutable[offset:end]

    # 3. 根据数据类型返回对应的闭包
    # 这种分支只执行一次，不会影响后续解析时的性能
    if data_bytes is not None:
        return _read_from_immutable
    else:
        return _read_from_mutable

def is_content_in_file(
    file_path: str, 
    search_content: str, 
    whole_word: bool = False, 
    case_sensitive: bool = True,
    is_regex: bool = False
) -> bool:
    """
    判断文件中是否包含特定内容。

    参数:
        file_path: 文件路径
        search_content: 搜索的内容（字符串或正则表达式）
        whole_word: 是否匹配独立单词 (仅对非正则或简单正则有效，默认 False)
        case_sensitive: 是否区分大小写 (默认 True)
        is_regex: 输入内容是否已经是正则表达式 (默认 False)

    返回:
        bool: 如果找到内容返回 True，否则返回 False
    """
    
    # 1. 检查文件是否存在，避免 FileNotFoundError
    file = Path(file_path)
    if not file.is_file():
        return False

    # 2. 构建正则表达式
    pattern = search_content
    
    if not is_regex:
        # 如果不是正则，先对特殊字符进行转义，防止报错
        pattern = re.escape(pattern)
        
        # 如果要求独立单词，添加单词边界符 \b
        if whole_word:
            pattern = r'\b' + pattern + r'\b'

    # 3. 设置编译标志
    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE

    try:
        # 编译正则以提高循环内的匹配效率
        compiled_regex = re.compile(pattern, flags)
        
        # 4. 逐行读取文件 (处理大文件时不会占用过多内存)
        # 使用 'utf-8' 编码，如果遇到二进制文件或编码错误，可以加 errors='ignore'
        with file.open('r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if compiled_regex.search(line):
                    return True
                    
    except Exception as e:
        print(f"读取文件出错: {e}")
        return False

    return False


def is_content_in_files(
    file_paths: List[Union[str, Path]], 
    search_content: str, 
    whole_word: bool = False, 
    case_sensitive: bool = True,
    is_regex: bool = False
) -> List[Path]:
    """
    在多个文件中搜索内容，返回包含该内容的文件路径列表。

    参数:
        file_paths: 文件路径列表 (支持字符串或 pathlib.Path 对象)
        search_content: 搜索的内容
        whole_word: 是否匹配独立单词
        case_sensitive: 是否区分大小写
        is_regex: 输入是否为正则表达式

    返回:
        List[Path]: 包含匹配内容的文件路径列表 (转换为 pathlib.Path 对象)
    """
    
    matched_files = []
    
    # 1. 预编译正则表达式
    # 在所有文件搜索前只编译一次，提高效率
    pattern = search_content
    if not is_regex:
        pattern = re.escape(pattern)
        if whole_word:
            pattern = r'\b' + pattern + r'\b'
            
    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE
        
    try:
        compiled_regex = re.compile(pattern, flags)
    except re.error as e:
        print(f"正则表达式编译错误: {e}")
        return []

    # 2. 遍历文件列表
    for file_path in file_paths:
        # 确保转换为 Path 对象，方便处理
        path_obj = Path(file_path)
        
        # 检查文件是否存在且是文件（排除目录）
        if not path_obj.is_file():
            continue
            
        try:
            # 3. 逐行读取并匹配
            # 使用 utf-8 编码，忽略无法解码的字符
            with open(path_obj, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if compiled_regex.search(line):
                        matched_files.append(path_obj)
                        break  # 找到后跳出当前文件的循环，继续下一个文件
                        
        except Exception as e:
            # 可以选择打印错误，或者静默跳过
            # print(f"无法读取文件 {path_obj}: {e}")
            continue

    return matched_files


def is_contents_in_files(
    file_paths: List[Union[str, Path]], 
    search_contents: List[str],  # 修改点：接收列表
    whole_word: bool = False, 
    case_sensitive: bool = True,
    is_regex: bool = False
) -> List[Path]:
    """
    在多个文件中搜索内容，只要包含 search_contents 列表中的任意一个内容，
    即返回该文件路径。

    参数:
        file_paths: 文件路径列表 (支持字符串或 pathlib.Path 对象)
        search_contents: 搜索内容列表 (List[str])
        whole_word: 是否匹配独立单词
        case_sensitive: 是否区分大小写
        is_regex: 输入是否为正则表达式

    返回:
        List[Path]: 包含匹配内容的文件路径列表
    """
    
    matched_files = []
    
    # 1. 构建正则表达式
    # 核心逻辑：使用正则的 "或" (|) 操作符连接所有关键字
    
    if not search_contents:
        return []
        
    pattern_parts = []
    
    for content in search_contents:
        if not content:
            continue
            
        if is_regex:
            # 如果是正则模式，直接添加，但为了安全建议包裹非捕获组
            # 防止类似 "a|b" 变成 "(a|b)..." 时破坏优先级
            pattern_parts.append(f"(?:{content})")
        else:
            # 如果是普通文本，先进行转义
            escaped_content = re.escape(content)
            if whole_word:
                escaped_content = r'\b' + escaped_content + r'\b'
            pattern_parts.append(escaped_content)
            
    if not pattern_parts:
        return []

    # 使用 "|" 连接所有部分，形成 "A|B|C" 的结构
    final_pattern = "|".join(pattern_parts)
    
    # 设置正则标志
    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE
        
    try:
        compiled_regex = re.compile(final_pattern, flags)
    except re.error as e:
        print(f"正则表达式编译错误: {e}")
        return []

    # 2. 遍历文件列表
    for file_path in file_paths:
        path_obj = Path(file_path)
        
        # 检查文件是否存在且是文件
        if not path_obj.is_file():
            continue
            
        try:
            # 3. 逐行读取并匹配
            with open(path_obj, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if compiled_regex.search(line):
                        matched_files.append(path_obj)
                        break  # 当前文件只要匹配到一个，就加入列表并跳出当前文件循环
                        
        except Exception as e:
            # 静默跳过无法读取的文件
            continue

    return matched_files