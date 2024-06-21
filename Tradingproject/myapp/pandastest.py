import pandas as pd
import numpy as np

 
dates = pd.date_range("20130101", periods=6)
a= [2,23,41,431,143]
df = pd.DataFrame(a, index=dates, columns=list("ABCD"))
print(df)