# Importing libraries
import yfinance as yf
import csv
import time
import logging

# Debugging
# logging.basicConfig(level=logging.DEBUG)

# FEATURE TITLES

general = ['symbol', 'currentPrice', 'sharesOutstanding']
features_add = ['trailingEps', 'forwardEps', 'lastDividendValue']  # dollar/share
features_add_perSO = ['freeCashflow', 'operatingCashflow', 'totalRevenue'] # dollar, divide by 'sharesOutstanding'
features_mult = [ 'shortRatio', 'beta', 'profitMargins', 'revenueGrowth', 'earningsGrowth', # ratios
                  'debtToEquity', 'priceToSalesTrailing12Months', 'returnOnEquity'] # ratios2
features_mult_perSO = ['averageVolume', 'sharesShort'] # percentage out of SO

investor_sentiment_factors = ['trailingPE', 'forwardPE', 'priceToBook', 'dividendYield'] # ratios

features_all = general + features_add + features_add_perSO + features_mult + features_mult_perSO + investor_sentiment_factors

# ACQUIRING AND ORGANIZING DATA

BIGDATA = []
with open('S&Ptickers', 'r') as file:
    for line in file:
        line = line.strip()
        data = []
        info = yf.Ticker(line).info
        for feature in general: # Following if-else in loops are bits of error correction, the rest is done in excel
            if(feature == 'sharesOutstanding' and info.get(feature, None) == None):
                if(info.get('marketCap', None) != None and info.get('currentPrice', None) != None):
                    data.append(int(info['marketCap'] / info['currentPrice']))
                else:
                    data.append(None)
            else:
                data.append(info.get(feature, None))
        for feature in features_add:
            if(feature == 'trailingEps' and info.get(feature, None) == None):
                if(info.get('forwardEps', None) != None):
                    data.append(info['forwardEps'])
                else:
                    data.append(None)
            elif (feature == 'forwardEps' and info.get(feature, None) == None):
                if (info.get('trailingEps', None) != None):
                    data.append(info['trailingEps'])
                else:
                    data.append(None)
            elif (feature == 'lastDividendValue' and info.get(feature, None) == None):
                data.append(0)
            else:
                data.append(info[feature])
        for feature in features_add_perSO:
            data_point = info.get(feature, None)
            if(data_point == None and feature == 'freeCashflow'):
                if(info.get('operatingCashflow', None) != None):
                    data_point = info['operatingCashflow']
            if (data_point == None and feature == 'operatingCashflow'):
                if (info.get('freeCashflow', None) != None):
                    data_point = info['freeCashflow']
            if(data_point == None):
                data.append(data_point)
            else:
                new_data = round(float(data_point)/float(data[2]), 5)
                data.append(new_data)
        for feature in features_mult:
            if(feature == 'earningsGrowth' and info.get(feature, None) == None):
                if(info.get('revenueGrowth', None) != None):
                    data.append(info['revenueGrowth'])
                else:
                    data.append(None)
            elif(feature == 'revenueGrowth' and info.get(feature, None) == None):
                if (info.get('earningsGrowth', None) != None):
                    data.append(info['earningsGrowth'])
                else:
                    data.append(None)
            elif (feature == 'profitMargins' and info.get(feature, None) == None):
                if (info.get('operatingMargins', None) != None):
                    data.append(info['operatingMargins'])
                else:
                    data.append(None)
            elif (feature == 'returnOnEquity' and info.get(feature, None) == None):
                if (info.get('returnOnAssets', None) != None):
                    data.append(info['returnOnAssets'])
                else:
                    data.append(None)
            else:
                data.append(info.get(feature, None))
        for feature in features_mult_perSO:
            data_point = info.get(feature, None)
            if (data_point == None and feature == 'averageVolume'):
                if (info.get('volume', None) != None):
                    data_point = info['volume']
            if (data_point == None and feature == 'sharesShort'):
                if (info.get('shortRatio', None) != None and info.get('volume', None) != None):
                    data_point = info['shortRatio'] * info['volume']
            if (data_point == None):
                data.append(data_point)
            else:
                new_data = round(float(data_point) / float(data[2]), 5)
                data.append(new_data)
        for feature in investor_sentiment_factors:
            if (feature == 'dividendYield' and info.get(feature, None) == None):
                data.append(0)
            elif (feature == 'trailingPE' and info.get(feature, None) == None):
                if (info.get('forwardPE', None) != None):
                    data.append(info['forwardPE'])
                else:
                    data.append(None)
            elif (feature == 'forwardPE' and info.get(feature, None) == None):
                if (info.get('trailingPE', None) != None):
                    data.append(info['trailingPE'])
                else:
                    data.append(None)
            elif (feature == 'priceToBook' and info.get(feature, None) == None):
                if (info.get('priceToSalesTrailing12Months', None) != None):
                    data.append(info['priceToSalesTrailing12Months'])
                else:
                    data.append(None)
            else:
                data.append(info.get(feature, None))
        BIGDATA.append(data)
        time.sleep(1) # Add delay

with open('trainingData_Ver1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(features_all) # header
    writer.writerows(BIGDATA) # data

# end

