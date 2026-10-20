import pandas as pd

df = pd.read_csv("data/horses.csv")

print(df)

print("\nTop Horse:")

print(df.iloc[0])