#include <iostream>
#include <vector>


namespace my {
    
template<typename T>
class List {
public:
    void append(T t) {
        std::cout<<"append base called"<<std::endl;
        _data.push_back(t);
    }
private:
    std::vector<T> _data;
};

template<>
class List<void*> {
public:
    void append(void *t) {
        std::cout<<"append void * called"<<std::endl;
        _data.push_back(t);
    }
private:
    std::vector<void*> _data;
};

template<typename T>
class List<T*> {
public:
    void append(T *t) {
        std::cout<<"append pointer type called"<<std::endl;
        _data.append(t);
    }
private:
    List<void*> _data;
};

}

int main(int argc, char **argv) {
    my::List<int> intList;
    intList.append(1);

    int a;
    my::List<int*> intList2;
    intList2.append(&a);
    return 0;
}