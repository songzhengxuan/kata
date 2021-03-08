#include <tbb/task_scheduler_init.h>
#include <tbb/task.h>
#include <iostream>

long SerialFib(long n) {
    if (n == 1 || n == 2) {
        return 1;
    }
    return SerialFib(n - 1) + SerialFib(n - 2);
}

const int CutOff = 16;
class FibTask : public tbb::task {
public:
    const long n;
    long* const sum;
    FibTask(long n_, long *sum_):n(n_),sum(sum_) {
    }
    task* execute() {
        if (n < CutOff) {
            *sum = SerialFib(n);
        } else {
            long x, y;
            FibTask &a = *new(tbb::task::allocate_child()) FibTask(n - 1, &x);
            FibTask &b = *new(tbb::task::allocate_child()) FibTask(n - 2, &y);
            set_ref_count(3);
            spawn(b);
            spawn_and_wait_for_all(a);
            *sum = x + y;
        }
        return NULL;
    }
};

long parallelFib(long n) {
    long sum;
    FibTask&a = *new(tbb::task::allocate_root()) FibTask(n, &sum);
    tbb::task::spawn_root_and_wait(a);
    return sum;
}

int main(int argc, char**argv) {
    int op = atoi(argv[1]);
    int n = atoi(argv[2]);
    if (op > 0) {
        std::cout<<parallelFib(n)<<std::endl;
    } else {
        std::cout<<SerialFib(n)<<std::endl;
    }
    return 0;
}