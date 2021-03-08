#include <iostream>
using namespace std;

class Person {
public:
    Person() {
        cout<<"Person constructor called"<<endl;
    }
};

int main(int argc, char **argv) {
    Person *p = new Person;
    Person *pArr = new Person[2];
    Person * ar =(Person *) ::operator new(sizeof(Person));
    delete p;
    delete []pArr;
    delete ar;
    return 0;
}