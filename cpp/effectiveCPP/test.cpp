#include <iostream>
using namespace std;
class Person {
public:
    Person(int _age):age(_age){}
    int age;
};

void foo(Person &p) {
    cout<<p.age<<endl;
}


int main(int argc, char **argv) {
    foo(Person(1));
    return 0;
}