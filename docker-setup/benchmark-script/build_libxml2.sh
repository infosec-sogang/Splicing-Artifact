#!/bin/bash

INSTALL_DIR="/build_output"
OUTPUT_BIN="xml2_read_fuzzer"

rm -rf "$INSTALL_DIR"/*
rm -rf ./libxml2
cp -r /benchmark/src/libxml2 ./

cd libxml2
./autogen.sh \
	--with-http=no \
	--with-python=no \
	--with-lzma=yes \
	--with-threads=no \
	--disable-shared || exit 1
make -j$(nproc) clean
make -j$(nproc) all || exit 1
cp /workspace/harness/libxml2/libxml2_xml_read_memory_fuzzer.cc ./

$CXX $CXXFLAGS -Iinclude/ -I"./src/" \
    libxml2_xml_read_memory_fuzzer.cc -o $OUTPUT_BIN \
    .libs/libxml2.a $LDFLAGS $LIBS -lm -lz -llzma || exit 1

cp "./$OUTPUT_BIN" "$INSTALL_DIR/" || exit 1
