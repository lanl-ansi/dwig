rm data/*.qh
rm data/*.json

../dwpg.py -cd 1 -rs 0 ran > data/ran1_i_0.qh
../dwpg.py -cd 1 -rs 0 -form ising ran > data/ran1_i_1.json
../dwpg.py -cd 1 -rs 0 -form binary ran > data/ran1_b_1.json
../dwpg.py -cd 1 -rs 0 -form ising ran -f > data/ran1_i_2.json
../dwpg.py -cd 1 -rs 0 -form ising ran -s 4 > data/ran4_i_0.json
