cmake_minimum_required(VERSION 3.10)
project(sfml_arcade_quest)

set(CMAKE_CXX_STANDARD 17)

# Find SFML
find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

# Main project
add_executable(sfml_arcade_quest src/main.cpp)
target_link_libraries(sfml_arcade_quest sfml-graphics sfml-window sfml-system)

# Sandbox
add_executable(sandbox sandbox/sandbox.cpp)
target_link_libraries(sandbox sfml-graphics sfml-window sfml-system)