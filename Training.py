import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb


train = pd.read_csv('trainingData_Ver1.csv', delimiter = ',') # read file
training_data = train.drop(['symbol', 'currentPrice', 'sharesOutstanding'], axis=1) # isolate feature data

target = train['currentPrice']

dTrain = xgb.DMatrix(training_data, label=target)
dEval = xgb.DMatrix(training_data, label=target)
error = {} # Data on root MSE

# hyperparameters
params = {
    'objective': 'reg:squarederror',  # Regression problem
    'max_depth': 6,
    'eta': 0.01,                       # Learning rate
    'eval_metric': 'rmse'             # Root Mean Squared Error for evaluation
}

iterations = 1725 # date of training, number of iterations
earlyStop = 172

model = xgb.train(params, # training parameters
                  dTrain, # data
                  iterations, # iterations
                  evals = [(dTrain, 'train'), (dEval, 'eval')], # error evaluation
                  evals_result = error, # error data array
                  # prev_model = input_model # old model
                  early_stopping_rounds = earlyStop)

model.save_model('modelVer1.json') # save the model

train_rmse = error['train']['rmse']
val_rmse = error['eval']['rmse']

iterations_arr = range(1, len(train_rmse) + 1)

# Plot RMSE vs iterations
plt.figure(figsize=(10, 6))
plt.plot(iterations_arr, [x**2 for x in train_rmse], label="Train MSE", color='blue')  # MSE is the square of RMSE
plt.plot(iterations_arr, [x**2 for x in val_rmse], label="Validation MSE", color='red')  # MSE is the square of RMSE
plt.xlabel('Iterations (Boosting Rounds)')
plt.ylabel('Mean Squared Error (MSE)')
plt.title('MSE vs Iterations')
plt.legend()
plt.grid(True)
plt.show()



