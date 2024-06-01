import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import pickle
import matplotlib.pyplot as plt

data=pd.read_csv("Cancer.csv")
print(data)

print(data.isnull().sum())

features=data.drop("diagnosis",axis="columns")
print(features)
target=data["diagnosis"]
print(target)

x_train,x_test,y_train,y_test=train_test_split(features,target)

model=DecisionTreeClassifier()
model.fit(features,target)

cr=classification_report(y_test,model.predict(x_test))
print(cr)

f=open("db.model","wb")
pickle.dump(model,f)
f.close()

print(model.feature_importances_)
x=features.columns
y=model.feature_importances_
plt.figure(figsize=(15,7))
plt.barh(x,y)
plt.show()