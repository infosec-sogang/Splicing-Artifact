#!/bin/bash

set -euxo pipefail

INSTALL_DIR="/build_output"

rm -rf "$INSTALL_DIR"/*
rm -rf ./libncurses
cp -r /benchmark/src/libncurses ./

cd libncurses
CONFIG_OPTIONS="--disable-shared --without-debug --without-manpages \
                --enable-termcap --prefix=/tmp/ncurses-install"
./configure $CONFIG_OPTIONS || exit 1
make -j"$(nproc)" || exit 1
make install V=1 || exit 1

cp /tmp/ncurses-install/bin/tic "$INSTALL_DIR/tic" || exit 1
cp /tmp/ncurses-install/bin/infotocap "$INSTALL_DIR/infotocap" || exit 1
