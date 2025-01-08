import pandas as pd
import xgboost as xgb
import numpy as np

model = xgb.Booster()
model.load_model('modelVer1.json')

test = pd.read_csv('trainingData_Ver1.csv', delimiter = ',') # read file
testing_data = test.drop(['symbol', 'currentPrice', 'sharesOutstanding'], axis=1) # rerun with training data

dtesting_data = xgb.DMatrix(testing_data)

predictions = model.predict(dtesting_data) # model outputs
tickers = test['symbol'].to_numpy() # ticker identifiers
real_prices = test['currentPrice'].to_numpy()

results = np.column_stack((tickers, predictions, real_prices))

df = pd.DataFrame(results, columns=['symbol', 'output', 'real_price'])

df.to_csv('testingResults.csv', index=False)

