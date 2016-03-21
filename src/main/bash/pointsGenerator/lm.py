import random
from sklearn import linear_model
import numpy as np
import pandas as pd

lambda1, lambda2 = 3.2, 0.6

def genR(lambda1, lambda2):
	target, val2 = random.randint(1, 1000), random.uniform(1, 100) 
	val1 = ((target - lambda2*val2) / lambda1) * (1 + random.uniform(-0.1, 0.1)) 
	return (target, val1, val2)

points = [genR(lambda1, lambda2) for x in range(10000)]

ft = np.array([[x[1], x[2]] for x in points])
lbl = np.array([x[0] for x in points])

regr = linear_model.LinearRegression(fit_intercept=False)

regr.fit(ft, lbl)

print lambda1, lambda2
print regr.intercept_, regr.coef_

pd.DataFrame(points).to_csv("points.csv", header=False, index=False)
