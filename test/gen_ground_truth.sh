rm data/*.json
rm data/*.qh
rm data/*.qubo

../dwig.py -cd  1 -rs 0 ran > data/ran1_i_1.json
../dwig.py -cd  1 -rs 0 ran -f > data/ran1_i_2.json
../dwig.py -cd  1 -rs 0 ran -s 4 > data/ran4_i_0.json
../dwig.py -cd 12 -rs 0 ran > data/ran1_i_3.json

../dwig.py -cd  2 -rs 0 fl > data/fl_i_1.json
../dwig.py -cd  2 -rs 0 fl -s 4 -a 0.3 > data/fl_i_2.json
../dwig.py -cd  2 -rs 0 fl -mc -mll 0 > data/fl_i_3.json
../dwig.py -cd 12 -rs 0 fl > data/fl_i_4.json

../dwig.py -cd 6 -rs 0 wscn > data/wscn_i_1.json
../dwig.py -cd 9 -rs 0 wscn > data/wscn_i_2.json
../dwig.py -cd 12 -rs 0 wscn > data/wscn_i_3.json

for file in $(find data -name *.json); do
    cat $file | ../bqp2qh.py > ${file//.json/.qh}
    cat $file | ../spin2bool.py | ../bqp2qubo.py > ${file//.json/.qubo}
    cat $file | ../bqp2mzn.py > ${file//.json/.mzn}
done