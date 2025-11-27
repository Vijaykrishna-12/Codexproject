import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sample.csv")

average_value = df["Value"].mean()
print("Average Value:", average_value)

plt.figure(figsize=(6,4))
plt.bar(df["Category"], df["Value"])
plt.xlabel("Category")
plt.ylabel("Value")
plt.title("Bar Chart")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
plt.scatter(df["Value"], df["Score"])
plt.xlabel("Value")
plt.ylabel("Score")
plt.title("Scatter Plot")
plt.tight_layout()
plt.show()

corr = df.corr(numeric_only=True)
plt.figure(figsize=(5,4))
plt.imshow(corr, interpolation='nearest')
plt.xticks(range(len(corr)), corr.columns)
plt.yticks(range(len(corr)), corr.columns)
plt.colorbar()
plt.title("Heatmap")
plt.tight_layout()
plt.show()
