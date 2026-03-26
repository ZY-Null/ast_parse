// 原始代码 - 包含各种测试场景
#include <iostream>
#include <string>
#include <vector>

// 全局变量
int global_counter = 0;
const char* APP_NAME = "OldApp";
static double pi_value = 3.14;

// 命名空间 Alpha
namespace Alpha {
    int namespace_var = 100;
    
    void process(int x) {
        std::cout << "Alpha::process(int): " << x << std::endl;
    }
    
    void helper() {
        std::cout << "Alpha::helper()" << std::endl;
    }
    
    class Calculator {
    public:
        int add(int a, int b) {
            return a + b;
        }
        
        double compute(double x) {
            return x * 2.0;
        }
    };
}

// 命名空间 Beta
namespace Beta {
    void process(const std::string& str) {
        std::cout << "Beta::process(string): " << str << std::endl;
    }
    
    void display() {
        std::cout << "Beta::display()" << std::endl;
    }
}

// 全局函数 - 将被替换
void initialize() {
    std::cout << "Initializing OLD system..." << std::endl;
    global_counter = 1;
}

// 重载函数集合
void process_data(int data) {
    std::cout << "Processing int: " << data << std::endl;
}

void process_data(double data) {
    std::cout << "Processing double: " << data << std::endl;
}

void process_data(const std::string& data) {
    std::cout << "Processing string: " << data << std::endl;
}

// 工具类
class Utility {
public:
    static void log(const std::string& message) {
        std::cout << "[LOG] " << message << std::endl;
    }
    
    static int max(int a, int b) {
        return (a > b) ? a : b;
    }
    
    // 旧版本的方法
    void old_method() {
        std::cout << "This method is outdated" << std::endl;
    }
};

// 简单类
class DataPoint {
private:
    int id;
    double value;
    
public:
    DataPoint(int id, double val) : id(id), value(val) 
    {}
    void
     test_printf() 
     const {
        std::cout << "DataPoint[" << id << "] = " << value << std::endl;
    


    }
    
    double get_value() const {
        return value;
    }
};

// 模板函数
template<typename T>
T square(T x) {
    return x * x;
}

// 内联函数
inline int increment(int x) {
    return x + 1;
}

template <class ...ARGS>
void test_printf(const char *fmt, ARGS...args){
    printf(fmt, std::forward<ARGS>(args)...);
    return;
}

namespace Bageyalu{
    void NsFunctiondef(){
        return;
    }
    void Bageyalu::OutNsFunction();
}
void Bageyalu::OutNsFunction(){
    return;
}

using namespace Bageyalu;

// 1. 普通函数
void normalFunction(int arg) {
    std::cout << "普通函数: " << arg << std::endl;
}

// 2. 模板函数
template<typename T>
void templateFunction(T arg) {
    std::cout << "模板函数: " << arg << std::endl;
}

// 类定义
class Example {
private:
    int value;
    static int staticValue;
    
public:
    // 3. 普通成员函数
    void memberFunction() {
        std::cout << "成员函数: " << value << std::endl;
    }
    
    // 带参数的成员函数
    void memberFunctionWithArg(int val) {
        value = val;
    }
    
    // 4. 静态函数
    static void staticFunction() {
        std::cout << "静态函数: " << staticValue << std::endl;
    }
    
    // 5. 模板成员函数
    template<typename T>
    void templateMemberFunction(T arg) {
        std::cout << "模板成员函数: " << arg << std::endl;
    }
    
    // 6. 静态模板函数
    template<typename T>
    static void staticTemplateFunction(T arg) {
        std::cout << "静态模板函数: " << arg << std::endl;
    }
    
    // 7. const成员函数
    void constMemberFunction() const {
        std::cout << "const成员函数: " << value << std::endl;
    }
    
    // 8. 重载成员函数
    void overloadedFunction() {
        std::cout << "重载版本1" << std::endl;
    }
    
    void overloadedFunction(int x) {
        std::cout << "重载版本2: " << x << std::endl;
    }
    
    // 9. 返回引用的成员函数
    int& getValueRef() {
        return value;
    }
    
    // 10. 返回const引用的成员函数
    const int& getValueConstRef() const {
        return value;
    }
    
    // 构造函数和析构函数
    Example() : value(0) {}
    explicit Example(int v) : value(v) {}
    ~Example() = default;
    
    // 11. 移动构造函数 (C++11)
    Example(Example&& other) noexcept : value(other.value) {}
    
    // 12. 拷贝赋值运算符
    Example& operator=(const Example& other) {
        if (this != &other) {
            value = other.value;
        }
        return *this;
    }
    
    // 13. 移动赋值运算符 (C++11)
    Example& operator=(Example&& other) noexcept {
        if (this != &other) {
            value = other.value;
        }
        return *this;
    }
};

// 静态成员初始化
int Example::staticValue = 100;

// 14. 函数模板特化
template<>
void templateFunction<std::string>(std::string arg) {
    std::cout << "特化的模板函数: " << arg << std::endl;
}

// 15. 函数对象（仿函数）
struct Functor {
    void operator()(int x) const {
        std::cout << "函数对象: " << x << std::endl;
    }
    
    template<typename T>
    void operator()(T x) const {
        std::cout << "模板函数对象: " << x << std::endl;
    }
};

// 16. lambda表达式 (C++11)
auto lambda = [](int x) { 
    std::cout << "Lambda函数: " << x << std::endl; 
};

// 17. 返回auto的函数 (C++11)
auto autoReturnFunction(int x) -> int {
    return x * 2;
}

// 18. decltype用于返回类型 (C++11)
template<typename T, typename U>
auto decltypeFunction(T t, U u) -> decltype(t + u) {
    return t + u;
}

// 19. 可变参数模板函数 (C++11)
template<typename... Args>
void variadicTemplateFunction(Args... args) {
    std::cout << "可变参数模板函数" << std::endl;
}

// 20. 默认参数函数
void defaultArgFunction(int x = 10, double y = 3.14) {
    std::cout << "默认参数函数: " << x << ", " << y << std::endl;
}

// 21. 内联函数
inline void inlineFunction() {
    std::cout << "内联函数" << std::endl;
}

// 22. noexcept函数 (C++11)
void noexceptFunction() noexcept {
    std::cout << "noexcept函数" << std::endl;
}

// 23. 委托构造函数 (C++11)
class DelegatingConstructor {
private:
    int a, b;
public:
    DelegatingConstructor() : DelegatingConstructor(0, 0) {}
    DelegatingConstructor(int x) : DelegatingConstructor(x, 0) {}
    DelegatingConstructor(int x, int y) : a(x), b(y) {}
};

// 24. 友元函数
class FriendExample {
private:
    int secret;
public:
    FriendExample() : secret(42) {}
    
    friend void friendFunction(const FriendExample& obj) {
        std::cout << "友元函数访问私有成员: " << obj.secret << std::endl;
    }
};

int main() {

    std::cout << "Old Main Function" << std::endl;
    
    initialize();
    process_data(42);
    process_data(3.14);
    
    Alpha::Calculator calc;
    std::cout << "Result: " << calc.add(5, 3) << std::endl;


    // 测试各种函数形式
    normalFunction(42);
    
    templateFunction(100);
    templateFunction(std::string("Hello"));
    
    Example ex;
    ex.memberFunction();
    ex.memberFunctionWithArg(50);
    ex.memberFunction();
    
    Example::staticFunction();
    
    ex.templateMemberFunction("Template Member");
    Example::staticTemplateFunction("Static Template");
    
    const Example constEx;
    constEx.constMemberFunction();
    
    ex.overloadedFunction();
    ex.overloadedFunction(99);
    
    Functor func;
    func(123);
    func("Hello Functor");
    
    lambda(456);
    
    defaultArgFunction();
    defaultArgFunction(20, 2.71);
    
    inlineFunction();
    noexceptFunction();
    
    friendFunction(FriendExample());

    return 0;
}