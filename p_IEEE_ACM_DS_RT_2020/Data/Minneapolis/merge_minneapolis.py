import pandas as pd
import os

minneapolis = pd.DataFrame()
try:
	os.remove('Minneapolis.csv')
except FileNotFoundError:
	pass

for file in os.listdir('.'):
	if 'csv' in file:
		print(file)
		minneapolis = minneapolis.append(pd.read_csv(file), sort=False)
minneapolis.to_csv('Minneapolis.csv', index=False)