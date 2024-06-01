import pickle

f=open("db.model","rb")
model = pickle.load(f)
f.close()

rm=float(input("enter raduis mean "))
tm=float(input("enter texture mean "))
pm=float(input("enter perimeter mean "))
am=float(input("enter area mean "))
sm=float(input("enter smoothness mean "))
com=float(input("enter compactness mean "))
conm=float(input("enter concavity mean "))
concm=float(input("enter concave points mean "))
sym=float(input("enter symmetry mean "))
fdm=float(input("enter fractal dimension mean "))

d=[[rm,tm,pm,am,sm,com,conm,concm,sym,fdm]]

result = model.predict(d)
print(result[0])