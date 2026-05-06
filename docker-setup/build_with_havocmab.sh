#!/bin/bash

mkdir -p /benchmark/bin/havocmab

export CC="/fuzzer/havocmab/afl-clang-fast"
export CFLAGS="-g -fno-omit-frame-pointer -fsanitize=address"
export CXX="/fuzzer/havocmab/afl-clang-fast++"
export CXXFLAGS="-g -fno-omit-frame-pointer -fsanitize=address"

./build_libtiff.sh || exit 1
cp /build_output/* /benchmark/bin/havocmab/ || exit 1

./build_binutils.sh || exit 1
cp /build_output/* /benchmark/bin/havocmab/ || exit 1

./build_libxml2.sh || exit 1
cp /build_output/* /benchmark/bin/havocmab/ || exit 1

./build_libpng.sh || exit 1
cp /build_output/* /benchmark/bin/havocmab/ || exit 1

./build_cyclonedds.sh || exit 1
cp /build_output/* /benchmark/bin/havocmab/ || exit 1

./build_libncurses.sh || exit 1
cp /build_output/* /benchmark/bin/havocmab/ || exit 1
