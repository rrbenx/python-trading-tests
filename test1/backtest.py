#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score

import warnings; warnings.simplefilter('ignore') # Importamos el modulo warnings y desactivamos los avisos para evitar flood

from array import array

symbol = sys.argv[1]
profit = float(sys.argv[2])

print("Calculating Total Hurst for %s" % symbol)

data = pd.read_csv("data-hurst/%s.csv" % symbol)

# Calculate phony vars
phony1 = array('d')
phony2 = array('d')
phony3 = array('d')
phony4 = array('d')
phony5 = array('d')
phony6 = array('d')
phony7 = array('d')
phony8 = array('d')
phony9 = array('d')

realopenval = array('d')
realcloseval = array('d')
openval = array('d')
closeval = array('d')
highval = array('d')
lowval = array('d')
openrel = array('d')
closerel = array('d')
diffrel = array('d')
hurst = array('d')
difhurst = array('d')
mean5 = array('d')
mean10 = array('d')
mean15 = array('d')
mean30 = array('d')
mean60 = array('d')
std5 = array('d')
std10 = array('d')
std15 = array('d')
std30 = array('d')
std60 = array('d')

for i in range(0, len(data)):
    if data.loc[i]["hurst"] != -1.0:
        realopenval.append(data.loc[i]["open"])
        realcloseval.append(data.loc[i]["close"])

        openval.append(data.loc[i]["mm_open"])
        closeval.append(data.loc[i]["mm_close"])
        highval.append(data.loc[i]["mm_high"])
        lowval.append(data.loc[i]["mm_low"])

        openrel.append(data.loc[i]["rel_open"])
        closerel.append(data.loc[i]["rel_close"])
        diffrel.append(data.loc[i]["rel_diff"])
        hurst.append(data.loc[i]["hurst"])
        difhurst.append(data.loc[i]["diff_hurst"])

        mean5.append(data.loc[i]["mean5"])
        mean10.append(data.loc[i]["mean10"])
        mean15.append(data.loc[i]["mean15"])
        mean30.append(data.loc[i]["mean30"])
        mean60.append(data.loc[i]["mean60"])

        std5.append(data.loc[i]["std5"])
        std10.append(data.loc[i]["std10"])
        std15.append(data.loc[i]["std15"])
        std30.append(data.loc[i]["std30"])
        std60.append(data.loc[i]["std60"])

        print("Frame: %i (%f)" % (i, profit))

        if data.loc[i]["diff_day1"] > profit:
            phony1.append(1)
        else:
            phony1.append(0)

X = pd.DataFrame()
X["open"] = openval
X["close"] = closeval
X["high"] = highval
X["low"] = lowval
X["diff"] = diffrel
X["diffhurst"] = difhurst
X["hurst"] = hurst
X["mean5"] = mean5
X["mean10"] = mean10
X["mean15"] = mean15
X["mean30"] = mean30
X["mean60"] = mean60
X["std5"] = std5
X["std10"] = std10
X["std15"] = std15
X["std30"] = std30
X["std60"] = std60

y = pd.DataFrame()
y["phony1"] = phony1

model = LogisticRegression()
model = model.fit(X, y)

print("Model score: %f" % model.score(X, y))

print("Running backtest...")
next_buy = False
wallet = 1000
shares = 0
buy_state = True
for i in range(0, len(X)):
    #if next_buy is set... buy on open and sell on close

    if next_buy and buy_state:
        buy_state = False
        shares = wallet / realopenval[i]
        wallet = 0
        print(" --- ")
        print("BUY  o: %f c: %f Wallet: %f Shares: %f" % (realopenval[i], realcloseval[i], wallet, shares));
        print(" --- ")
    else:
        if not buy_state and realopenval[i] < realcloseval[i-1]:
            buy_state = True
            wallet = realcloseval[i] * shares
            shares = 0
            print(" --- ")
            print("SELL o: %f c: %f Wallet: %f Shares: %f" % (realopenval[i], realcloseval[i], wallet, shares));
            print(" --- ")


    c = model.predict(X.loc[i].reshape(-1, 17))
    p = model.predict_proba(X.loc[i].reshape(-1, 17))
    print("%i  o: %f, c: %f, d: %f, h: %f dh: %f" % (i, openval[i], closeval[i], diffrel[i], hurst[i], difhurst[i]))

    if c == 1:
        next_buy = True
    else:
        next_buy = False

print("Wallet: %f ratio: %f" % (wallet, wallet / 1000.0));
