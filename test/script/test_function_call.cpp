#include <bits/stdc++.h>
using namespace std;

template <typename T>
T DoSomething(T const &val)
{
    return val + 1;
}

class CTest{
public:
    static CTest &GetInst();
    static int StaticFunction(uint32_t);
    int NormalFunction();
};

uint64_t FooDoSomething();


int foo1();
int foo2();
int foo3();
int foo4();

using FOO = int *();

string FunctionTestCall()
{
    // 1. normal
    auto v = FooDoSomething();

    uint32_t v1 = ((v >> 32) & 0xFFFFFFFF);
    uint32_t v2 = (v & 0xFFFFFFFF);

    // 2, template
    auto v3 = DoSomething(v2);

    auto v4 = DoSomething<uint64_t>(0x1234);


    // 3, member
    CTest cObj;
    auto v5 = cObj.NormalFunction();

    // 4, static
    auto v6 = CTest::StaticFunction(v1);
    auto v7 = CTest::GetInst().NormalFunction();

    // 5, multi level
    auto v8 = DoSomething(CTest::StaticFunction(v2));

    map<int, FOO> handlers = {
        {1, foo1},
        {2, foo2},
        {3, foo3},
        {4, foo4},
    };

    for(auto &p: handlers)
    {
        if(p.first != v1)
        {
            continue;
        }
        auto var = (p.second)();
    }

    stringstream ss;
    ss << "v  = " << v << "\n"
       << "v1 = " << v1 << "\n"
       << "v2 = " << v2 << "\n"
       << "v3 = " << v3 << "\n"
       << "v4 = " << v4 << "\n"
       << "v5 = " << v5 << "\n"
       << "v6 = " << v6 << "\n"
       << "v7 = " << v7 << "\n"
       << "v8 = " << v8 << "\n"
       << endl;
    return ss.str();
}

int main(int argc, char const *argv[])
{
    /* code */
    return 0;
}
