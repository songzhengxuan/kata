#include <iostream>
using namespace std;
class Base {
protected:
  int foo;
public:
  virtual int method(int p) {
      cout<<"base method called"<<endl;
    return foo + p;
  }
};

class Base2 {
protected:
    int foo;
public:
    virtual int method2(int p) {
        cout<<"base2 method 2 called"<<endl;
        return foo+p;
    }
};

struct Point {
  double cx, cy;
};

class Derived : public Base, Base2{
public:
  virtual int method(int p) {
      cout<<"Derived method called"<<endl;
    return Base::foo + bar + p;
  }
protected:
  int bar, baz;
  Point a_point;
  char c;
};

class BB {
public:
    virtual void foo() {

    }
    virtual void bar() {

    }
};

class B1 : virtual public BB {
public:
    virtual void foo() {

    }
};

class B2 : virtual public BB {
public:
    virtual void bar() {

    }
};

class Child : public B1, B2 {
public:
    void foo() {

    }

    void bar() {

    }
};

using vfp= void (*)();

int main(int argc, char** argv) {
    Base *bp = new Derived;
    bp->method(0);
    cout<<"sizeof(Derived)"<<sizeof(Derived)<<endl;
    cout<<"sizeof(Child)"<<sizeof(Child)<<endl;
    Child c;
    printf("B1 is %p, B2 is %p\n", (B1*)(&c), (B2*)(&c));
    printf("B1.BB is %p, B2.BB is %p\n", (BB*)((B1*)(&c)), (BB*)((B2*)(&c)));

    return 0;
}