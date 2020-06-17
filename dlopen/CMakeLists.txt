cmake_minimum_required(VERSION 3.2)

project("fancylib")

add_library(fancylib
    SHARED
    fancylib.c
)

add_library(goodlib
    SHARED
    goodlib.c
)

target_link_libraries(fancylib
    goodlib
)

add_executable(
    demo
    userprog.cpp
)