#include<iostream>
using namespace std;

class Base {
public:
    int pubMember;
    void pubFoo() {}
protected:
    int protectedMember;
    void protectedFoo() {}
private:
    int privateMember;
    void privateFoo() {}
};

class Derived : private Base {
public:
    void derivedFoo() {
        Base::pubFoo();
        Base::protectedFoo();
    }
};


int main(int argc, char **argv) {
    Derived d;
    d.derivedFoo();
    return 0;
}