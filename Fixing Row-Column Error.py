#Step 1: Importing all the necessary packages for fixing row-column error
import pandas as pd
import matplotlib.pyplot as plt
import pickle as pkl
import csv
import json

#Step 2: Loading the dataset from your local machine
df = pd.read_csv('/Users/Desktop/file_location/file.csv')
df

#Step 3: Transposing the data to interchange row and column
df1 = df.T
df1

#Step 4: Saving the error free file again in the CSV format
# Read the file in the same location mentioned in Step 2
df1.to_csv(r'/Users/Desktop/file_location/file.csv')

#Step 5: Checking the converted file to make sure it is free of errors
df2 = pd.read_csv('/Users/Desktop/file_location/file.csv')
df2