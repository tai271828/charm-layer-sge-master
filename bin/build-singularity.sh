#!/bin/bash
VERSION=2.5.2
wget https://github.com/singularityware/singularity/releases/download/$VERSION/singularity-$VERSION.tar.gz
tar xvf singularity-$VERSION.tar.gz
cd singularity-$VERSION
./configure --prefix=/usr/local
make
make install

singularity pull shub://tai271828/solvcon:1.0.0-0.1.4+ /home/ubuntu/
