#include <iostream>
#include <vector>
using namespace std;

namespace my {
class WidgetImpl {
public:
    WidgetImpl(int para) {
        a = b = c = para;
    }

private:
    int a, b,c;
    std::vector<double> v;
};

class Widget {
public:
    Widget(const Widget &rhs) {
        *pImpl = *(rhs.pImpl);
    }

    Widget& operator=(const Widget &rhs) {
        *pImpl = *(rhs.pImpl);
        return *this;
    }

    Widget(int para) {
        pImpl = new WidgetImpl(para);
    }

private:
    WidgetImpl *pImpl;
};

void swap(Widget &lhs, Widget &rhs) {
    cout<<"swap called"<<endl;
}

template <typename A, typename B>
class Spe {
public:
    void setA(const A &a) {
        cout<<"setA 1"<<endl;
        this->a = a;
    }

    void setB(const B &b) {
        cout<<"setB 1"<<endl;
        this->b = b;
    }
private:
    A a;
    B b;
};

template<typename A>
class Spe<A, int> {
public:
    void setA(const A &a) {
        cout<<"setA 2"<<endl;
        this->a = a;
    }
    void setB(const int &b) {
        cout<<"setB 2"<<endl;
        this->b = b;
    }
private:
    A a;
    int b;
};

}// end of my

template<typename T>
void foo(T &lhs, T &rhs) {
    cout<<"foo general"<<endl;
    swap(lhs, rhs);
}

template<>
void foo<my::Widget>(my::Widget &lhs,my::Widget &rhs){
    cout<<"foo widget"<<endl;
    swap(lhs, rhs);
}

void bar(my::Widget lhs, my::Widget rhs) {
    foo(lhs, rhs);
}


int main(int argc, char **argv) {
    bar(1, 2);
    my::Spe<int, float> a;
    a.setA(0);
    a.setB(0);
    return 0;
}