import ctypes  
ll = ctypes.cdll.LoadLibrary   
lib = ll("/Users/song/github/tbb/python/libpycall.so")    
lib.foo(1, 3)  
print '***finish***'