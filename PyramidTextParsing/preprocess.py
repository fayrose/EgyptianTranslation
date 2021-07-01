import pandas as pd

df = pd.read_csv('combined.csv', index_col=0)

df.to_csv('standardized.csv')