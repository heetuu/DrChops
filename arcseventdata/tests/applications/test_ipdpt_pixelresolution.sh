#!/usr/bin/env bash

rm -f Ipdpt.h5
ipdpt.py -o Ipdpt.h5 --pixel-resolution=2 -n 50000 -t -0,16000,100 -x ARCS.xml events.dat

./compareHistogram.py "Ipdpt.h5/I(pdpt)" "oracle/Ipdpt-p2.h5/I(pdpt)"
