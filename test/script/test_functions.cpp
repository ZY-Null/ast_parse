#include <vector>
#include <type_traits>
#include <limits>
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

/*  */
/* comments?s */
/* good */
template <typename T>
size_t GetLen()
{
    return sizeof(T);
}
/* ujeyhwfbewruydhveruiwefuihwdefhiunjeujhnefujhikhjkdsfkjjksadklaskshdbsdm
sdasjkdhkjasdas
dsadjskadasdsa */
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

/* 这个是啥？ */
template uint8_t PlusOne<uint8_t, uint16_t>(uint8_t a, uint16_t b);

/* 这个是啥？ */
template<> uint16_t PlusOne<uint16_t, uint16_t>(uint16_t a, uint16_t b);

/* vecvtor? */
template <typename T>
using VECT = std::vector<T>;

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

int main(int argc, char const *argv[])
{
    normal_function_1();
    return 0;
}
