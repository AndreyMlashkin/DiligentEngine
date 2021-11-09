cmake_minimum_required(VERSION 3.1)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

get_cmake_property(_variableNames VARIABLES)
list (SORT _variableNames)
foreach (_variableName ${_variableNames})
message(STATUS "${_variableName}=${${_variableName}}")
endforeach()

add_executable(test_package test_package.cpp)
target_link_libraries(test_package ${CONAN_LIBS})
