# python-trading-tests (Python trading related exercises)

STEP 1

getvals.py: Download data from SP500 symbols
```
python getvals.py
```
It lasts a while, about... 80 mins.

STEP 2

hurst.py: Calculate the hurst index for previously downloaded data

usage:
```
python hurst.py <symbol>
```
example:
```
python hurst.py MMM
```
note:
 <symbol> must be a valid symbol with its ".csv" file previously downloaded

note2:
 This operation is quite heavy, so... let's "parallel" it with a oneliner bash spell! (-j4 indicates that 4 is the max number of processes to use)

run in shell:
```
for file in $(ls data/*.csv); do basename $file; done | sed "s/.csv//" | parallel -j4 "python hurst.py {}"
```

STEP 3

backtest.py: Run the backtest for the previously calculated values
