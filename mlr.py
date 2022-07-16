import pandas as pd
from sklearn import linear_model
import pickle

gn = pd.read_csv("data.csv")

X = gn[["Force", "Angle", "Resistance"]]
y = gn['Target']


reg = linear_model.LinearRegression()

reg.fit(X.values,y.values)

predicted_target = reg.predict([[70, 82, 2.7]])
print(predicted_target)
print(reg.coef_)


filename = 'gunny.sav'
pickle.dump(reg, open(filename, 'wb'))