import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

#Import Data
dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values

#Normalaziation 
sc = MinMaxScaler(feature_range = (0,1))
training_set_scaled = sc.fit_transform(training_set)

#Last three months (60 timesteps)
X_train = []
Y_train = []
 
for i in range(60 , 1258):
    X_train.append(training_set_scaled[i-60:i ,0])
    Y_train.append(training_set_scaled[i,0])
    
X_train , Y_train = np.array(X_train) , np.array(Y_train)

#Reshape
X_train = np.reshape(X_train,(X_train.shape[0] , X_train.shape[1] ,1 ))
 


#Create RNN
regressor = Sequential()
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1] ,1 )))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

#Output layer 
regressor.add(Dense(units = 1))

#Compile the Rnn
regressor.compile(optimizer = 'adam' , loss = 'mean_squared_error')

#Fit 
regressor.fit(X_train , Y_train, epochs = 100, batch_size=32 )

#Making the prediction
dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

dataset_total = pd.concat((dataset_train['Open'] , dataset_test['Open']) , axis = 0 )
inputs = dataset_total[len(dataset_total) - len(dataset_test) -60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = [] 
for i in range(60 , 80):
    X_test.append(inputs[ i-60 : i , 0 ])
    
X_test = np.array(X_test)
X_test = np.reshape(X_test,(X_test.shape[0] , X_test.shape[1] ,1 ))
predicted_stock_price = regressor.predict(X_test)
#Inverse scaling 
predicted_stock_price = sc.inverse_transform(predicted_stock_price)


#Visualising
plt.plot(real_stock_price,color = 'red',label = 'Real Google Stock Price')
plt.plot(predicted_stock_price,color = 'blue',label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()










