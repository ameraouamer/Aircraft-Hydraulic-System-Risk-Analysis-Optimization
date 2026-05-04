import pandas as pd
from /home/amer/Aviation_Sim/Data_generation/synthetic_generator.py import HydraulicDataGenerator

generator = HydraulicDataGenerator()
data= generator.generate()

df=pd.dataframe(data)
df.to_csv("data.csv")
print(df.head())