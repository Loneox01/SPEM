import pandas as pd

sp = pd.read_csv('S&P500.csv', delimiter = ',') # import ticker list
tickers = sp['Symbol'] # get symbols
tickers_py = tickers.tolist() # convert to python list

with open('S&Ptickers', 'w') as file:
    for t in tickers_py:
        file.write(f"{t}\n")