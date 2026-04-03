from pydantic import BaseModel

def calculate_match_score(list1: list, list2: list):
    # 1. 检查空列表情况
    if not list1 or not list2:
        return 0
    
    # 2. 检查最后一个元素
    if list1[-1] != list2[-1]:
        return 0
    
    match_point = 1
    l2_pivot = len(list2) - 2
    for l1_pivot in range((len(list1) - 1), -1, -1):
        if l2_pivot < 0:
            break
        t_value = list1[l1_pivot]
        l2_cursor = l2_pivot
        for l2_index in range(l2_cursor, -1, -1):
            if list2[l2_index] != t_value:
                continue
            match_point += 1
            l2_pivot = l2_index - 1
            break
    return match_point


class TestCase(BaseModel):
    l1: list
    l2: list
    exp: int

test_cases: list = [
    {
        "l1": [],
        "l2": [],
        "exp": 0,
    },
    {
        "l1": [1, 4, 5],
        "l2": [],
        "exp": 0,
    },
    {
        "l1": [],
        "l2": [4, 8, 6],
        "exp": 0,
    },
    {
        "l1": [1, 2, 3, 4, 5],
        "l2": [1, 2, 3],
        "exp": 0,
    },
    {
        "l1": [1,5,3,9],
        "l2": [1,3,9],
        "exp": 3,
    },
    {
        "l1": [1, 2, 3, 4, 5, 6, 8],
        "l2": [8],
        "exp": 1,
    },
    {
        "l1": [1, 2, 3, 4, 5, 6, 8],
        "l2": [3, 8],
        "exp": 2,
    },
    {
        "l1": [1, 2, 3, 4, 5, 6, 8],
        "l2": [4, 1, 2, 8],
        "exp": 2,
    },
]
for c in test_cases:
    obj = TestCase.model_validate(c)
    m = calculate_match_score(obj.l1, obj.l2)
    if m != obj.exp:
        print(f"[ERROR] {obj.l1} match {obj.l2} = {m} != {obj.exp}")