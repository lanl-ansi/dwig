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

../dwig.py -ic -pp -cd 12 -tl -rs 0 fclg -gf 0.1 -mll 5 -a 0.1 > data/fclg_i_1.json
../dwig.py -ic -pp -cd 13 -tl -rs 0 fclg -gf 0.2 > data/fclg_i_2.json
../dwig.py -ic -pp -cd 14 -tl -rs 0 fclg -gf 0.3 -mll 0 > data/fclg_i_3.json
../dwig.py -ic -pp -cd 15 -tl -rs 0 fclg -gf 0.4 -sgs -s 2 > data/fclg_i_4.json
../dwig.py -ic -pp -cd 16 -tl -rs 0 fclg -gf 0.5 -sgs > data/fclg_i_5.json

../dwig.py -ic -pp -tl -rs 0 -cd 8 xran -cv " -5,-1,1" -cw 2,1,1 > data/xran_i_1.json
../dwig.py -ic -pp -tl -rs 0 -cd 12 xran -cv " -3,-1,1,3" -cw 7,1,1,7 > data/xran_i_2.json
../dwig.py -ic -pp -tl -rs 0 -cd 16 xran -cv " -1,-0.5,0,0.5,1" -cw 3,1.5,1,2,2.5 > data/xran_i_3.json
../dwig.py -ic -pp -tl -rs 0 -cd 16 xran -cv " -1,1" -cw 1,1 -f -fv " -1,1" -fw 1,1> data/xran_i_4.json
../dwig.py -ic -pp -tl -rs 0 -cd 12 xran -cv 1,2,3,4 -cw 0,1,0,1 -f -fv " -3,4" -fw 1,2 > data/xran_i_5.json
../dwig.py -ic -pp -tl -rs 0 -cd 8 xran -cv 4,3,2,1 -cw 0,0,1,2 -f -fv 3,2.5 -fw 5,1 > data/xran_i_6.json
../dwig.py -ic -pp -tl -rs 0 -cd 10 xran > data/xran_i_7.json
