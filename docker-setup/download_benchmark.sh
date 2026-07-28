#!/bin/bash

mkdir /benchmark/src
cd /benchmark/src

# libtiff
wget https://download.osgeo.org/libtiff/tiff-4.2.0.tar.gz || exit 1
tar -xf tiff-4.2.0.tar.gz
rm tiff-4.2.0.tar.gz
mv tiff-4.2.0 libtiff

# binutil
wget https://ftp.gnu.org/gnu/binutils/binutils-2.37.tar.gz || exit 1
tar -xf binutils-2.37.tar.gz
rm binutils-2.37.tar.gz
mv binutils-2.37 binutils

# libxml2
wget https://download.gnome.org/sources/libxml2/2.9/libxml2-2.9.12.tar.xz || exit 1
tar -xf libxml2-2.9.12.tar.xz
rm libxml2-2.9.12.tar.xz
mv libxml2-2.9.12 libxml2

# libpng
git clone --branch libpng17 --single-branch https://github.com/pnggroup/libpng.git || exit 1

# cyclonedds
git clone https://github.com/eclipse-cyclonedds/cyclonedds.git || exit 1
cd cyclonedds
git checkout 53cf7c
cd ..

# libncurses-6.4
wget https://invisible-mirror.net/archives/ncurses/ncurses-6.4.tar.gz || exit 1
tar -xzf ncurses-6.4.tar.gz
rm ncurses-6.4.tar.gz
mv ncurses-6.4 libncurses
