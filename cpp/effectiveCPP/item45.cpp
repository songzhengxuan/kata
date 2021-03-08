#include <iostream>
class Top {

};

class Middle : public Top {

};

class Bottom : public Middle {

};

template<typename T>
class SmartPtr {
public:
    explicit SmartPtr(T* realPtrr) {
        m_ptr = realPtr;
    }
private:
    T* m_ptr;
};

int main(int argc, char **argv) {
    Top *ptr = new Middle;
    SmartPtr<Top> pt1 = SmartPtr<Middle>(new Midddle);
    return 0;
}
