#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *
import sys
import pandas as pd
from sklearn import preprocessing

import warnings; warnings.simplefilter('ignore') # Importamos el modulo warnings y desactivamos los avisos para evitar flood

from array import array

def hurst(ts):
    """Returns the Hurst Exponent of the time series vector ts"""
    # Creamos el rango de los valores de demora
    lags = range(10, 500)

    # Calculamos la matriz de varianzas de las diferencias de las demoras
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # Usamos un ajuste lineal para estimar el exponente de Hurst
    poly = polyfit(log(lags), log(tau), 1)

    # Devolvemos el exponente de Hurst obtenido del ajuste lineal
    return poly[0]*2.0

symbol = sys.argv[1]

print("Calculating Total Hurst for %s" % symbol)

data = pd.read_csv("data/%s.csv" % symbol)
hurst_calc = hurst(data['adjusted_close'].dropna())

print("Hurst value: %f" % hurst_calc)

limit = 1000

print("Calculating Dinamic Hurst for %s" % symbol)
rel_open = array('d')
rel_close = array('d')
rel_diff = array('d')
mm_open = array('d')
mm_close = array('d')
mm_high = array('d')
mm_low = array('d')
rel_mean5 = array('d')
rel_mean10 = array('d')
rel_mean15 = array('d')
rel_mean30 = array('d')
rel_mean60 = array('d')
rel_std5 = array('d')
rel_std10 = array('d')
rel_std15 = array('d')
rel_std30 = array('d')
rel_std60 = array('d')
tmp_hurst_calc = array('d')
diff_hurst_calc = array('d')
tmp_hurst_calc1 = array('d')
tmp_hurst_calc2 = array('d')
tmp_hurst_calc3 = array('d')
tmp_hurst_calc4 = array('d')
tmp_hurst_calc5 = array('d')
tmp_hurst_calc6 = array('d')
tmp_hurst_calc7 = array('d')
tmp_hurst_calc8 = array('d')
tmp_hurst_calc9 = array('d')

for i in range(0, limit):
    rel_open.append(-1)
    rel_close.append(-1)
    rel_diff.append(-1)
    mm_open.append(-1)
    mm_close.append(-1)
    mm_high.append(-1)
    mm_low.append(-1)
    rel_mean5.append(-1)
    rel_mean10.append(-1)
    rel_mean15.append(-1)
    rel_mean30.append(-1)
    rel_mean60.append(-1)
    rel_std5.append(-1)
    rel_std10.append(-1)
    rel_std15.append(-1)
    rel_std30.append(-1)
    rel_std60.append(-1)
    tmp_hurst_calc.append(-1)
    diff_hurst_calc.append(-1)
    tmp_hurst_calc1.append(-1)
    tmp_hurst_calc2.append(-1)
    tmp_hurst_calc3.append(-1)
    tmp_hurst_calc4.append(-1)
    tmp_hurst_calc5.append(-1)
    tmp_hurst_calc6.append(-1)
    tmp_hurst_calc7.append(-1)
    tmp_hurst_calc8.append(-1)
    tmp_hurst_calc9.append(-1)

for i in range(limit, len(data) - 9):

    tmp_array_close = data["adjusted_close"].dropna()[i - limit:i]
    tmp_array_open = data["open"].dropna()[i - limit:i]
    tmp_array_high = data["high"].dropna()[i - limit:i]
    tmp_array_low = data["low"].dropna()[i - limit:i]
    #print(tmp_array)

    #standarize data
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_close = min_max_scaler.fit_transform(tmp_array_close.reshape(limit, -1))
    min_max_open = min_max_scaler.fit_transform(tmp_array_open.reshape(limit, -1))
    min_max_low = min_max_scaler.fit_transform(tmp_array_low.reshape(limit, -1))
    min_max_high = min_max_scaler.fit_transform(tmp_array_high.reshape(limit, -1))

    last5 = min_max_close[:-5]
    last10 = min_max_close[:-10]
    last15 = min_max_close[:-15]
    last30 = min_max_close[:-30]
    last60 = min_max_close[:-60]

    mm_open.append(asscalar(min_max_open[0][-1]))
    mm_close.append((min_max_close[0][-1]))
    mm_high.append((min_max_high[0][-1]))
    mm_low.append((min_max_low[0][-1]))

    rel_open.append(data.loc[i]["open"] / data.loc[i-1]["open"])
    rel_close.append(data.loc[i]["close"] / data.loc[i-1]["close"])
    rel_diff.append(data.loc[i-1]["close"] / data.loc[i-1]["open"])

    rel_mean5.append(mean(last5))
    rel_mean10.append(mean(last10))
    rel_mean15.append(mean(last15))
    rel_mean30.append(mean(last30))
    rel_mean60.append(mean(last60))
    rel_std5.append(std(last5))
    rel_std10.append(std(last10))
    rel_std15.append(std(last15))
    rel_std30.append(std(last30))
    rel_std60.append(std(last60))

    current_hurst = hurst(tmp_array_close)
    tmp_hurst_calc.append(current_hurst)
    diff_hurst_calc.append(tmp_hurst_calc[-1] - tmp_hurst_calc[-2])

    tmp_hurst_calc1.append(data.loc[i+1]["close"] - data.loc[i]["close"])
    tmp_hurst_calc2.append(data.loc[i+2]["close"] - data.loc[i]["close"])
    tmp_hurst_calc3.append(data.loc[i+3]["close"] - data.loc[i]["close"])
    tmp_hurst_calc4.append(data.loc[i+4]["close"] - data.loc[i]["close"])
    tmp_hurst_calc5.append(data.loc[i+5]["close"] - data.loc[i]["close"])
    tmp_hurst_calc6.append(data.loc[i+6]["close"] - data.loc[i]["close"])
    tmp_hurst_calc7.append(data.loc[i+7]["close"] - data.loc[i]["close"])
    tmp_hurst_calc8.append(data.loc[i+8]["close"] - data.loc[i]["close"])
    tmp_hurst_calc9.append(data.loc[i+9]["close"] - data.loc[i]["close"])

for i in range(0, 9):
     rel_open.append(-1)
     rel_close.append(-1)
     rel_diff.append(-1)
     mm_open.append(-1)
     mm_close.append(-1)
     mm_high.append(-1)
     mm_low.append(-1)
     rel_mean5.append(-1)
     rel_mean10.append(-1)
     rel_mean15.append(-1)
     rel_mean30.append(-1)
     rel_mean60.append(-1)
     rel_std5.append(-1)
     rel_std10.append(-1)
     rel_std15.append(-1)
     rel_std30.append(-1)
     rel_std60.append(-1)
     tmp_hurst_calc.append(-1)
     diff_hurst_calc.append(-1)
     tmp_hurst_calc1.append(-1)
     tmp_hurst_calc2.append(-1)
     tmp_hurst_calc3.append(-1)
     tmp_hurst_calc4.append(-1)
     tmp_hurst_calc5.append(-1)
     tmp_hurst_calc6.append(-1)
     tmp_hurst_calc7.append(-1)
     tmp_hurst_calc8.append(-1)
     tmp_hurst_calc9.append(-1)


print("Elements in data: %i hurst: %i" % (len(data), len(tmp_hurst_calc)))

data["hurst"] = tmp_hurst_calc
data["diff_hurst"] = diff_hurst_calc
data["rel_open"] = rel_open
data["rel_close"] = rel_close
data["rel_diff"] = rel_diff
data["mm_open"] = mm_open
data["mm_close"] = mm_close
data["mm_high"] = mm_high
data["mm_low"] = mm_low
data["mean5"] = rel_mean5
data["mean10"] = rel_mean10
data["mean15"] = rel_mean15
data["mean30"] = rel_mean30
data["mean60"] = rel_mean60
data["std5"] = rel_std5
data["std10"] = rel_std10
data["std15"] = rel_std15
data["std30"] = rel_std30
data["std60"] = rel_std60
data["diff_day1"] = tmp_hurst_calc1
data["diff_day2"] = tmp_hurst_calc2
data["diff_day3"] = tmp_hurst_calc3
data["diff_day4"] = tmp_hurst_calc4
data["diff_day5"] = tmp_hurst_calc5
data["diff_day6"] = tmp_hurst_calc6
data["diff_day7"] = tmp_hurst_calc7
data["diff_day8"] = tmp_hurst_calc8
data["diff_day9"] = tmp_hurst_calc9

data.to_csv("data-hurst/%s.csv" % symbol)
