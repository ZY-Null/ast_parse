在 Tree-Sitter 中，S-expression 查询（S表达式查询）是一种强大的工具，它能像“精准地图”一样，根据代码结构来搜索信息，而不是简单的文本匹配。下面我先介绍它的核心语法，然后提供一个完整的 Python 实现方案。

### 🧬 S-expression 查询核心语法

S-expression 查询的基本格式是 `(节点类型 (子节点…))`。为了让查询更精确，它提供了一系列语法元素：

| 语法元素 | 说明 | 示例 |
| :--- | :--- | :--- |
| **节点类型** | 直接使用 AST 中的节点名，如 `function_definition`。 | `(function_definition)` |
| **字段匹配** | 通过 `字段名:` 指定节点的特定子节点。 | `(function_definition name: (identifier))` |
| **嵌套模式** | 将 S-expression 嵌套，以描述节点间的层级关系。 | `(function_definition (statement_block))` |
| **节点捕获** | 使用 `@变量名` 来提取并命名你感兴趣的节点。 | `(identifier) @func_name` |
| **通配符** | 用 `_` 匹配任意类型的节点。 | `(call_expression function: (_) @call)` |
| **匿名节点** | 用 `"字符串"` 匹配像 `"("`, `"+"` 这样的符号。 | `(binary_expression operator: "+")` |
| **重复匹配** | `?` (0或1次)，`*` (0或多次)，`+` (1或多次)。 | `(parameter_list (parameter_declaration)+)` |
| **谓词系统** | 使用 `(#eq? @var "value")` 对捕获的节点内容进行精确文本匹配。 | `(#eq? @func_name "main")` |

### ⚙️ 环境准备与基础解析

在开始查询前，先要准备好 Python 环境并解析代码：

```python
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Node, Query, QueryCursor

# 1. 初始化语言和解析器
# 关键点：使用 Language(tscpp.language()) 来正确加载 C++ 语法。
CPP_LANGUAGE = Language(tscpp.language())
parser = Parser(CPP_LANGUAGE)

# 2. 解析 C++ 代码，获取语法树的根节点
code = b"""
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 3);
    return 0;
}
"""
tree = parser.parse(code)
root_node = tree.root_node
```

### 🎯 实现你的查询方法

下面我们基于刚刚解析的代码，实现你提出的两个查询需求。

#### 1. 全局查找 `function_declaration` 节点

在 `tree-sitter-cpp` 中，函数定义对应的节点类型是 `function_definition`。

```python
# 查询：匹配所有 function_definition 节点，并捕获其名称
query_str = """
    (function_definition
        declarator: (function_declarator
            declarator: (identifier) @func_name)) @func_def
"""
query = Query(CPP_LANGUAGE, query_str)
cursor = QueryCursor(query)

# 执行查询
func_defs = cursor.captures(root_node)

print("=== 找到的函数定义 ===")
for capture_name, node in func_defs:
    if capture_name == 'func_def':
        func_name_node = node.child_by_field_name('declarator')
        if func_name_node:
             # 函数名可能嵌套在更深层，使用我们捕获的 @func_name 会更可靠。
             # 这里我们直接打印，后续会展示如何通过查询直接提取。
             pass

# 更佳实践：直接从查询结果中获取捕获的函数名
func_names = cursor.captures(root_node) # cursor.captures 返回 (capture_name, node) 元组的列表
for capture_name, node in func_names:
    if capture_name == 'func_name':
        print(f"- {node.text.decode('utf8')}")
```

#### 2. 查找 `call_expression` 节点（作为 `function_definition` 的子节点）

这里需要区分两种情况：直接子节点和间接子节点（任意深度的后代节点）。

```python
# --- 2.1 查找直接子节点 ---
# 查询：匹配作为 function_definition 直接子节点的 call_expression
direct_query_str = """
    (function_definition
        body: (compound_statement
            (call_expression) @direct_call))
"""
direct_query = Query(CPP_LANGUAGE, direct_query_str)
direct_cursor = QueryCursor(direct_query)

direct_calls = direct_cursor.captures(root_node)

print("\n=== 直接位于函数体内的调用 ===")
for capture_name, node in direct_calls:
    if capture_name == 'direct_call':
        # 获取函数名节点
        func_node = node.child_by_field_name('function')
        if func_node:
            print(f"- {func_node.text.decode('utf8')}")


# --- 2.2 查找间接子节点 (任意深度) ---
# 方案：先查询出所有 function_definition，然后遍历它们，在每个函数节点上执行一个匹配所有 call_expression 的查询。

# 首先，创建一个匹配所有 call_expression 的查询
all_calls_query_str = "(call_expression) @all_call"
all_calls_query = Query(CPP_LANGUAGE, all_calls_query_str)

print("\n=== 函数体内任意深度的调用 ===")
# 复用之前找到的 func_defs
for capture_name, node in func_defs:
    if capture_name == 'func_def':
        func_name = node.child_by_field_name('declarator').text.decode('utf8')
        # 在当前函数节点（而非全局 root_node）上执行查询
        cursor = QueryCursor(all_calls_query)
        calls_inside_func = cursor.captures(node)

        if calls_inside_func:
            print(f"函数 {func_name} 内的调用:")
            for call_cap, call_node in calls_inside_func:
                func_node = call_node.child_by_field_name('function')
                if func_node:
                    print(f"  - {func_node.text.decode('utf8')}")
```

### 💡 进阶技巧与总结

*   **节点类型查询**：如果不确定 `tree-sitter-cpp` 的节点名称，可以先用简单的 `(expression) @exp` 捕获，然后打印 `node.type` 来探索。
*   **谓词过滤**：可以使用 `(#eq? @func_name "main")` 这样的谓词，精确筛选出名为 "main" 的函数，而不是所有函数。
*   **逻辑组合**：一个查询字符串可以包含多个模式，用 `[]` 包裹，如 `[ (call_expression) (new_expression) ]` 可以同时匹配函数调用和 `new` 表达式。

**总结**：Tree-sitter 的查询系统功能非常强大。通过结合节点类型、字段匹配和谓词系统，你可以精确地描述代码模式。对于复杂结构（如任意深度的嵌套），组合使用查询与手动遍历是最高效的策略。