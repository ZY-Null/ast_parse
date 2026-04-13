#include <bits/stdc++.h>
#include "some_head.hpp"

using namespace std;

template <typename T>
using DICT_MAP = std::map<uint32_t, T>;

typedef DICT_MAPPER = std::map<uint32_t, std::string>;

typedef void (*FUNC_PTR)(uint32_t a, uint32_t b);

uint32_t global_simple_val_no_init;
uint32_t global_simple_val = 0x1234;

std::list<uint> vars = {1, 2, 3, 4, 5, 6};

#define SOME_CONST (320U)

#define DELETE_SP_CONSTRUCTS(cls_name)              \
    cls_name(cls_name const &) = delete;            \
    cls_name(cls_name &&) = delete;                 \
    cls_name &operator=(cls_name const &) = delete; \
    cls_name &operator=(cls_name &&) = delete

#define SP_PRINT(fmt, ...) printf("[debug][%s][%d]" fmt, __func__, __LINE__, ##__VA_ARGS__)

void function_f1()
{
    SP_PRINT("asdasdasdasd");
}

char *GetDescription(uint32_t mark)
{
    return "guyhbqwuyghweduyghwe";
}

template <typename T>
std::list<T> GenList(size_t num)
{
    std::list<T> res;
    for (size_t i = 0; i < num; i++)
    {
        res.push_back(T());
    }
    return res;
}

class ClsDemo
{
public:
    ClsDemo() = default;
    DELETE_SP_CONSTRUCTS(ClsDemo);
    ~ClsDemo() = default;

    uint32_t foo() {
        return (uint32_t)printf(nullptr);
    }
};


namespace some_ns
{
    void foo()
    {
        printf("");
    }
}
