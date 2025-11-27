import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("train.csv")

cols = ["OverallQual", "GrLivArea", "TotalBsmtSF", "FullBath", "BedroomAbvGr", "YearBuilt", "Neighborhood", "SalePrice"]
df = df[cols].dropna()

df = pd.get_dummies(df, columns=["Neighborhood"], drop_first=True)

X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print("RMSE:", round(rmse, 2))
print("R2:", round(r2, 3))
print("Example actual vs predicted (first 10):")
for actual, pred in zip(y_test.values[:10], y_pred[:10]):
    print(int(actual), " -> ", int(pred))
