#include "fancylib.h"
#include "goodlib.h"

static int c = 1;

int foo(int a, int b) {
    int ret = a + b + bar(a, b);
    c *= 10;
    ret += c;
    return ret;
}