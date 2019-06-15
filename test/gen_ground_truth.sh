rm data/*.json

../dwig.py -ic -pp -cd  1 -tl -rs 0 -os const > data/const_i_1.json
../dwig.py -ic -pp -cd  1 -tl -rs 0 -os const -cp 0.2 > data/const_i_2.json
../dwig.py -ic -pp -cd  1 -tl -rs 0 -os const -cp 0.2 -f -0.5 > data/const_i_3.json
../dwig.py -ic -pp -cd 16 -tl -rs 0 -os const -cp 0.2 -f -0.5 > data/const_i_4.json
../dwig.py -ic -pp -ccb 1 1 2 5 -tl -rs 0 -os const -cp 0.2 -f -0.5 > data/const_i_5.json

../dwig.py -ic -pp -cd  1 -tl -rs 0 -os ran > data/ran1_i_1.json
../dwig.py -ic -pp -cd  1 -tl -rs 0 -os ran -f > data/ran1_i_2.json
../dwig.py -ic -pp -cd  1 -tl -rs 0 -os ran -s 4 > data/ran4_i_0.json
../dwig.py -ic -pp -cd 16 -tl -rs 0 -os ran > data/ran1_i_3.json
../dwig.py -ic -pp -ccb 1 1 2 5 -tl -rs 0 -os ran > data/ran1_i_4.json

../dwig.py -ic -pp -cd 1 -tl -rs 0 ran -pr 1.0 > data/rfm1_i_1.json
../dwig.py -ic -pp -cd 1 -tl -rs 0 ran -pr 1.0 -f > data/rfm1_i_2.json
../dwig.py -ic -pp -cd 1 -tl -rs 0 ran -pr 1.0 -f -s 4 > data/rfm4_i_1.json

../dwig.py -ic -pp -cd  2 -tl -rs 0 fl -sgs > data/fl_i_1.json
../dwig.py -ic -pp -cd  2 -tl -rs 0 fl -sgs -s 4 -a 0.3 > data/fl_i_2.json
../dwig.py -ic -pp -cd  2 -tl -rs 0 fl -sgs -mc -mll 0 > data/fl_i_3.json
../dwig.py -ic -pp -cd 16 -tl -rs 0 fl -sgs > data/fl_i_4.json
../dwig.py -ic -pp -cd  2 -tl -rs 0 fl > data/fl_i_5.json

../dwig.py -ic -pp -cd 6 -tl -rs 0 fl -sgs -ccc -a 0.1 > data/fcl_i_1.json
../dwig.py -ic -pp -cd 6 -tl -rs 0 fl -sgs -ccc -s 4 > data/fcl_i_2.json
../dwig.py -ic -pp -cd 16 -tl -rs 1 fl -sgs -ccc > data/fcl_i_3.json
../dwig.py -ic -pp -cd 6 -tl -rs 0 fl -ccc -a 0.1 > data/fcl_i_4.json

../dwig.py -ic -pp -cd 6 -tl -rs 0 wscn > data/wscn_i_1.json
../dwig.py -ic -pp -cd 9 -tl -rs 0 wscn > data/wscn_i_2.json
../dwig.py -ic -pp -cd 12 -tl -rs 0 wscn > data/wscn_i_3.json
../dwig.py -ic -pp -cd 16 -tl -rs 0 wscn > data/wscn_i_4.json

