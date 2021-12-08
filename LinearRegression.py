import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

results = pd.read_csv('results.csv', sep=',', names=['result', 'time', 'score', 'algorithm'])
expected = results[-6:]

results['algorithm'] = results['algorithm'].map({'minimax': 0, 'expectimax': 1})
results['result'] = results['result'].map({'defeat': 0, 'victory': 1})

test = results[-6:]
results = results[:-6]
X = results[['result', 'time', 'algorithm']]
y = results['score']

linreg = LinearRegression()
linreg.fit(X, y)

predicted = linreg.predict(test[['result', 'time', 'algorithm']])
expected['predicted'] = predicted.astype(int)
expected = expected[['result', 'time', 'algorithm', 'score', 'predicted']]
print(expected)
expected.to_csv('prediction.csv', sep=',', index=False)