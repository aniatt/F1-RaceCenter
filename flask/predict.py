import numpy as np
import pandas as pd
import pickle
import requests
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# HELPER FUNCTION
def tryconvert(x):
    try:
      if str(x) == '00.000':
        return 0 
      else:
       if x != 0:
         return (float(str(x).split(':')[1]) + (60 * float(str(x).split(':')[0])))
       else: 
         return 0
    except:
      return 0
  
# GET RAW DATA VIA ERGAST F1 API
def getInput(raceYear, roundNum):
  df_train = pd.read_csv('data/dummy.csv')
  df = pd.DataFrame().reindex(columns = df_train.columns)
  data = {column: [] for column in df}
  data.update( {'constructor' : []} )

  url = 'http://ergast.com/api/f1/'+ raceYear + '/' + roundNum + '/qualifying.json'
  r = requests.get(url)
  json = r.json()
  pos = 0

  for item in json['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
    try:
      data['season'].append(int(json['MRData']['RaceTable']['Races'][0]['season']))
    except:
      data['season'].append(None)

    try:
      data['round'].append(int(json['MRData']['RaceTable']['Races'][0]['round']))
    except:
      data['round'].append(None)

    try:
      data['circuit_id_' + json['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId']].append(1)
    except:
      try:
        data['circuit_id_' + json['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId']].append(0)
      except:
        pass

    try:
      data['driver'].append(item['Driver']['driverId'])
    except:
      data['driver'].append(None)

    try:
      data['constructor'].append(item['Constructor']['constructorId'])
    except:
      data['constructor'].append(None)

    try:
      data['qualifying_time'].append(item['Q3'])
    except:
      try:
        data['qualifying_time'].append(item['Q2'])
      except:
        try:
          data['qualifying_time'].append(item['Q1'])
        except:
          data['qualifying_time'].append(None)
    
    data['grid'].append(pos)
    pos += 1
  
  return data
  

# FORMAT INPUT (QUALI TIMES, CONSTRUCTORS)
def generateDataset(raceYear, roundNum):
  data = getInput(raceYear,roundNum)
  data = {k: [0] * len(data['season']) if not v else v for k, v in data.items()}

  cnt = 0
  for i in data['constructor']:
    try:
      data['constructor_' + i][cnt] = 1
      cnt += 1
    except:
      cnt += 1

  df = pd.DataFrame(data)
  df.drop('constructor', axis = 1, inplace = True)

  df['qualifying_time'] = df.qualifying_time.map(lambda x: tryconvert(x))
  df = df[df['qualifying_time'] != 0]
  df.sort_values(['season', 'round', 'grid'], inplace = True)
  df['qualifying_time_diff'] = df.groupby(['season', 'round']).qualifying_time.diff()
  df['qualifying_time'] = df.groupby(['season', 'round']).qualifying_time_diff.cumsum().fillna(0)
  df.drop('qualifying_time_diff', axis = 1, inplace = True)
  
  return df