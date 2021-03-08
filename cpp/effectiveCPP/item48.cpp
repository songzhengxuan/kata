#include <iostream>

template<int N>
class Factorial {
public:
    enum {value = N * Factorial<N - 1>::value};
};

template<>
class Factorial<0> {
public:
    enum {value = 1};
};

int main(int argc, char **argv) {
    std::cout<<Factorial<4>::value<<std::endl;
    return 0;
}
