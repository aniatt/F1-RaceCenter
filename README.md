# F1 Race Center
## Description
F1 Race Center will allow users to visualize a variety of Formula One relevant tools, ranging from 'Race Classification Prediction', 'Driver/Team Sentiment Analysis', and 'Historical Data'.

### Race Classification
##### Data
2014 - Present marks the Turbo - Hybrid era of Formula One. The Race Classifier seeks to train a model based on this historical data, and use that as a means to predict the finishing order of a given race given a few inputs. Currently, these inputs are qualifying pace/grid position, circuit, and constructor. ALL DATA IS CURRENTLY GATHERED FROM THE ERGAST F1 API.

##### ML Model
The model chosen for this project was a RandomForestClassifier. Keras GridSearch() was used to optimize parameters and ultimiately train the model. Training data currently ranges from 2014 - 2019. Test data is currently the 2020 Formula One Season.

The model was saved using Pickle - see here for note regarding usage (Section 9.1.1): https://scikit-learn.org/stable/model_persistence.html

##### Prediction
Prediction is done so by making use of predict.py once model is trained and saved.

INPUT: .csv file formatted just like training data (can be generated from processing.py to ensure compattible formatting). Input data includes qualifying pace (as a gap to the driver on pole position). circuit_id, and constructor (see processing.py, final_data.csv for more details).

OUTPUT: Currently, predict.py outputs a .txt file (or direct terimal output) that shows the starting grid for each race in a given season, alongside predictions based on RandomForestClassifier.

##### Results
F1 Predictor 2020 Season Accuracy: 9/17 winners correctly predicted.

Drawbacks: DNFs, weather, penalties are unpredictable in current state. Potential solution to account for this lies with incoorporation of Sentiment Analysis.

Improvements: More input variables (driver standings, constructor standings, free practice pace***)

### Sentiment Analysis
Goal: Develop a sentiment analysis model to go along with predictions, to enhance race weekend info for a given race.

### Historical Data
Goal: Access historical data given user's preference to compare against at an instant.

### Visualizer
Goal: Combine all these tools into a singular platform so user has easy access at all times and experience a well - designed UI.


## Usage
### Current State
1. Clone repository
2. Use processing.py (make changes as you see fit depending on range of data you would like to work with) for preprocessing and formatting. (ONLY DO THIS STEP IF YOU DO NOT WANT TO USE final_data.tsv as your training data)
3. Train RandomForestClassifier (ONLY DO THIS STEP IF YOU DO NOT WANT TO USE final_data.tsv as your training data)
4. Ensure cloned repository contains a trained model (located in the model folder)
5. Follow predict.py commands to execute script (Season and Round Number required)
6. Output results to .txt file / terminal

### TODO
Goal: Devolop visualizer where user has the ability to select a time period / race for which they wish to see predictions. Visualizer will also contain relevant sentiment for that race as well as relevant historical data / metadata.


## Relevant Info
Note: Inspiration and Data Processing Strategy referenced from https://towardsdatascience.com/formula-1-race-predictor-5d4bfae887da
