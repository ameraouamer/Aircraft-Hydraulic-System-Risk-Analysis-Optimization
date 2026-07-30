import pandas as pd
from synthetic_generator import HydraulicDataGenerator

generator = HydraulicDataGenerator()
data= generator.generate()

df=pd.DataFrame(data)
df.to_csv("data.csv")
print(df.head())