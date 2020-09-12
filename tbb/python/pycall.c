#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>
#include "process.h"
#ifdef __cplusplus
extern "C" {
#endif

int foo(int a, int b)  
{  
  printf("you input %d and %d\n", a, b);  
  return a+b;  
}  

int init(int width, int height, int * arr) {
  // generate random 
  return 0;
}

int process(int width, int height, int *arr) {
  // 
  int *dst = (int*) malloc(width * height * sizeof(int));
  do_process(width, height, arr, dst);
  memcpy(arr, dst, width * height * sizeof(int));
  free(dst);
  return 0;
}

#ifdef __cplusplus
}
#endif
