#include <type_traits>
#include "limits"
#include <cstdio>
#include <cstdint>

void normal_function_1(void)
{
    printf("[" __FILE_NAME__ "][%s] do nothing!\n", __func__);
}

const char *normal_function_2(int index)
{
    static char const *caches[] = {
        "庸主啊，庸主！",
        "竟然不许！",
        "战至最后一刻，自刎归天！",
        "死不可怕，死是凉爽的夏夜",
        "你拾它作甚！",
    };
    static size_t len = sizeof(caches) / sizeof(caches[0]);
    if(index < 0 || index >= len)
    {
        return "我寻思抢点钱，买大力";
    }
    return caches[index];
}

template <typename T>
size_t GetLen()
{
    return sizeof(T);
}

template <typename T1, typename T2>
T1 PlusOne(T1 a, T2 b)
{
    if(b > std::numeric_limits<T1>::max())
    {
        return std::numeric_limits<T1>::max();
    }
    if(a > (std::numeric_limits<T1>::max() - b))
    {
        return std::numeric_limits<T1>::max();
    }
    return a + b;
}

template <>
uint8_t PlusOne<uint8_t, uint16_t>(uint8_t a, uint16_t b) { return a + 1; };

template uint16_t PlusOne<uint16_t, uint16_t>(uint16_t a, uint16_t b);

namespace test_namespace
{
    void normal_nsfunction_1(void)
    {
        printf("[" __FILE_NAME__ "][%s] do nothing!\n", __func__);
    }

    const char *normal_nsfunction_2(int index)
    {
        return "The End!";
    }
}

uint32_t &GetRefData()
{
    static uint32_t s_data = 10036;
    return s_data;
}

int main(int argc, char const *argv[])
{
    normal_function_1();
    uint8_t a = 0xF1;
    uint16_t b = 0xFFFF, c = 0x1;
    auto r1 = PlusOne(a, b);
    auto r2 = PlusOne(b, c);
    GetRefData() = PlusOne((uint32_t)100, (uint32_t)200);
    printf("[" __FILE_NAME__ "][%s], r1=0x%02x, r2=0x%04x, R3=0X%08X\n", __func__, r1, r2, GetRefData());
    return 0;
}
