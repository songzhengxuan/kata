#include <iostream>
#include <dlfcn.h>
using namespace std;

static int foo_proxy(int a, int b);
typedef decltype(foo_proxy) *foo_ptr_t;
foo_ptr_t foo_ptr = nullptr;

void dotest() {
    void *handle = dlopen("libfancylib.dylib", RTLD_GLOBAL|RTLD_NOW);
    foo_ptr = (foo_ptr_t) dlsym(handle, "foo");
    cout<<handle<<endl;
    cout<<foo_ptr<<endl;
    cout<<"result"<<endl;
    cout<<foo_proxy(1, 1)<<endl;
    cout<<foo_proxy(1, 1)<<endl;
    cout<<foo_proxy(1, 1)<<endl;
    dlclose(handle);
    foo_ptr = nullptr;
}

int main(int argc, char **argv) {
    dotest();
    dotest();
    return 0;
}
static int foo_proxy(int a, int b) {
    if (foo_ptr != nullptr) {
        return (*foo_ptr)(a, b) ;
    }
    return 0;
}