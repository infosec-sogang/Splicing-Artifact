#!/bin/bash
cp -r /workspace/HavocMAB/fuzzers/Havoc_DMA /fuzzer/havocmab || exit 1
cd /fuzzer/havocmab || exit 1

patch -p3 < /workspace/havocmab_patch.diff
export LLVM_CONFIG=/usr/bin/llvm-config-12
make && cd llvm_mode && make
