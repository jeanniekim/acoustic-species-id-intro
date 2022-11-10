"""
Engineers for Exploration (E4E)
Acoustic Species ID Intro Project:
Stratified Random Sampling System
Jeannie Kim
11/4/22
"""

# libraries
import pandas as pd
import math
import random
import csv

# paths to CSVs for input and output
DATA_PATH = "Peru_2019_AudioMoth_Data_Full.csv"
OUTPUT_PATH = "samples.csv"

"""
Write a function that will take in csv path 
and output a new csv file with a stratified random sample of the original csv. 
Should return True/False if the stratified csv file was successful.
"""
def sample(path):

  df = pd.read_csv(path)
  df.dropna(subset=['Duration', 'Comment'], inplace=True) # dropping NaN*
  # *dependent on what you consider valid data

  # put the CSV data into a dictionary grouped by the AudioMothCodes
  # keys: audiomoth names, values: dataframes of the data for that audiomoth
  amDict = {g:x for g,x in df.groupby('AudioMothCode', sort=False)}

  badAms = {'AM-21', 'AM-19', 'AM-8', 'AM-28'}  # set of Audiomoths to ignore


  # Organizing the data

  # outer dict: keys = audiomoths, values = inner dicts
  # inner dict: keys = hour value (0-24), values = clips at hour 
  # (row of dataframe stored as list)
  finDict = dict()    # outer dict

  # for each audiomoth
  for am in amDict.keys():
    
    # skip Audiomoths we know are bad
    if am in badAms:
      continue

    # dataframe corresponding to current Audiomoth
    currAmDf = amDict[am]
    
    # initialize inner dict
    hourDict = dict()

    # for each row in Am dataframe
    for i, row in currAmDf.iterrows():  # index, row (series of tuples)

      # get hour and duration
      # new: from 'Comment' column*
      # comment example: "Recorded at 11:00:00 19/06/2022..."
      # *WWF Audiomoths don't have 'StartDateTime'

      comm = currAmDf['Comment'][i]
      time = str(comm).split()[2]
      hour = int(time.split(':')[0])

      duration = float(currAmDf['Duration'][i])
      
      # successful clip: duration must be >= a minute
      if (duration >= 60):
        
        if hour not in hourDict.keys(): # new hour
          # add it to inner dictionary
          hourDict[hour] = []

        # append the whole row (as an arr) to the
        # array (value) at that hour (key)
        hourDict[hour].append(row.values)

    # successful audiomoth: exists a valid clip for every hour
    if len(hourDict) == 24:
      
      # add the audiomoth to the final dictionary
      finDict[am] = hourDict


  # Sampling and writing to final CSV

  toWrite = []

  # for each valid audiomoth
  for am in finDict.keys():
    # for each hour
    for hour in finDict[am].keys():
      # get random clip
      toWrite.append(random.choice(finDict[am][hour]))
  
  # write to csv
  with open(OUTPUT_PATH, 'w', newline= '') as f:
      writer = csv.writer(f)
      writer.writerow(df.columns)
      writer.writerows(toWrite)


# call function
sample(DATA_PATH)
