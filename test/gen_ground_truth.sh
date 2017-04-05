rm data/*.json

../dwig.py -pp -cd  1 -tl -rs 0 -os ran > data/ran1_i_1.json
../dwig.py -pp -cd  1 -tl -rs 0 -os ran -f > data/ran1_i_2.json
../dwig.py -pp -cd  1 -tl -rs 0 -os ran -s 4 > data/ran4_i_0.json
../dwig.py -pp -cd 12 -tl -rs 0 -os ran > data/ran1_i_3.json

../dwig.py -pp -cd 1 -tl -rs 0 ran -pr 1.0 > data/rfm1_i_1.json
../dwig.py -pp -cd 1 -tl -rs 0 ran -pr 1.0 -f > data/rfm1_i_2.json
../dwig.py -pp -cd 1 -tl -rs 0 ran -pr 1.0 -f -s 4 > data/rfm4_i_1.json

../dwig.py -pp -cd  2 -tl -rs 0 fl -sgs > data/fl_i_1.json
../dwig.py -pp -cd  2 -tl -rs 0 fl -sgs -s 4 -a 0.3 > data/fl_i_2.json
../dwig.py -pp -cd  2 -tl -rs 0 fl -sgs -mc -mll 0 > data/fl_i_3.json
../dwig.py -pp -cd 12 -tl -rs 0 fl -sgs > data/fl_i_4.json
../dwig.py -pp -cd  2 -tl -rs 0 fl > data/fl_i_5.json

../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -cc -a 0.1 > data/fcl_i_1.json
../dwig.py -pp -cd 6 -tl -rs 0 fl -sgs -cc -s 4 > data/fcl_i_2.json
../dwig.py -pp -cd 12 -tl -rs 1 fl -sgs -cc > data/fcl_i_3.json
../dwig.py -pp -cd 6 -tl -rs 0 fl -cc -a 0.1 > data/fcl_i_4.json

../dwig.py -pp -cd 6 -tl -rs 0 wscn > data/wscn_i_1.json
../dwig.py -pp -cd 9 -tl -rs 0 wscn > data/wscn_i_2.json
../dwig.py -pp -cd 12 -tl -rs 0 wscn > data/wscn_i_3.json

