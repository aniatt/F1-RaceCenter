import pandas as pd
import numpy as np
import requests

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


def getRaces():
    races = {'season': [],
             'round': [],
             'circuit_id': [],
             'country': [],
             'date': [],
            }

    for year in list(range(2014,2021)):
        url = 'https://ergast.com/api/f1/{}.json'
        r = requests.get(url.format(year))
        json = r.json()

        for item in json['MRData']['RaceTable']['Races']:
            races['season'].append(int(item['season']))
            races['round'].append(int(item['round']))
            races['circuit_id'].append(item['Circuit']['circuitId'])
            races['country'].append(item['Circuit']['Location']['country'])
            races['date'].append(item['date'])
            
    races = pd.DataFrame(races)
    return races


def getQuali(rounds):
    quali = {'season': [],
             'round':[],
             'circuit_id':[],
             'driver': [],
             'qualifying_time': []
            }

    for n in list(range(len(rounds))):
        for i in rounds[n][1]:
            url = 'http://ergast.com/api/f1/{}/{}/qualifying.json'
            r = requests.get(url.format(rounds[n][0], i))
            json = r.json()
            
            for item in json['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
                quali['season'].append(int(json['MRData']['RaceTable']['Races'][0]['season']))
                quali['round'].append(int(json['MRData']['RaceTable']['Races'][0]['round']))
                quali['circuit_id'].append(json['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId'])
                quali['driver'].append(item['Driver']['driverId'])
                try:
                    quali['qualifying_time'].append(item['Q3'])
                except:
                    try:
                        quali['qualifying_time'].append(item['Q2'])
                    except:
                        try:
                            quali['qualifying_time'].append(item['Q1'])
                        except:
                            quali['qualifying_time'].append(None)
    
    quali = pd.DataFrame(quali)
    return quali


# MASTER FUNCTION
def getResults():
    # GET RACE INFORMATION
    races = getRaces()

    rounds = []
    for year in np.array(races.season.unique()):
        rounds.append([year, list(races[races.season == year]['round'])])

    # GET QUALI INFORMATION
    quali = getQuali(rounds)

    results = {'season': [],
               'round':[],
               'circuit_id':[],
               'driver': [],
               'constructor': [],
               'grid': [],
               'podium': []
              }

    for n in list(range(len(rounds))):
        for i in rounds[n][1]:
        
            url = 'http://ergast.com/api/f1/{}/{}/results.json'
            r = requests.get(url.format(rounds[n][0], i))
            json = r.json()

            for item in json['MRData']['RaceTable']['Races'][0]['Results']:
                results['season'].append(int(json['MRData']['RaceTable']['Races'][0]['season']))
                results['round'].append(int(json['MRData']['RaceTable']['Races'][0]['round']))
                results['circuit_id'].append(json['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId'])
                results['driver'].append(item['Driver']['driverId'])
                results['constructor'].append(item['Constructor']['constructorId'])
                results['grid'].append(int(item['grid']))
                results['podium'].append(int(item['position']))

    results = pd.DataFrame(results)

    return races, results, quali


def main():
    races, results, quali = getResults()

    # MERGING / DATA CONVERSION
    temp_df = pd.merge(races, results, how='inner', on=['season', 'round', 'circuit_id'])
    final_df = pd.merge(temp_df, quali, how='left', on=['season', 'round', 'driver', 'circuit_id']).drop(['date','country'], axis = 1)

    final_df['qualifying_time'] = final_df.qualifying_time.map(lambda x: tryconvert(x))
    final_df = final_df[final_df['qualifying_time'] != 0]
    final_df.sort_values(['season', 'round', 'grid'], inplace = True)
    final_df['qualifying_time_diff'] = final_df.groupby(['season', 'round']).qualifying_time.diff()
    final_df['qualifying_time'] = final_df.groupby(['season', 'round']).qualifying_time_diff.cumsum().fillna(0)
    final_df.drop('qualifying_time_diff', axis = 1, inplace = True)

    df_dum = pd.get_dummies(final_df, columns = ['circuit_id', 'constructor'])

    for col in df_dum.columns:
        if 'constructor' in col and df_dum[col].sum() < 140:
            df_dum.drop(col, axis = 1, inplace = True)
            
        elif 'circuit_id' in col and df_dum[col].sum() < 70:
            df_dum.drop(col, axis = 1, inplace = True)
        
        else:
            pass

    df_dum.to_csv('data/final_df.csv', index = False)

    return 0

if __name__ == "__main__":
    main()