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
Prediction is done so by running app.py and following prompts (SEE DEPLOYMENT UPDATES ON THIS PAGE). Predict.py outlines prediction framework/methods.

##### Results
F1 Predictor 2020 Season Accuracy: 9/17 winners correctly predicted.

Drawbacks: DNFs, weather, penalties are unpredictable in current state. Potential solution to account for this lies with incoorporation of Sentiment Analysis.

Improvements: More input variables (driver standings, constructor standings, FP pace/results)

### Sentiment Analysis (IN PROGRESS)
Goal: Develop a sentiment analysis model to go along with predictions, to enhance race weekend info for a given race.

### Historical Data
Goal: Access historical data given user's preference to compare against at an instant.

### Visualizer (IN PROGRESS)
Goal: Combine all these tools into a singular platform so user has easy access at all times and experience a well - designed UI.


## Usage
### Current State
1. Clone repository
2. cd flask
3. Execute app.py
4. Visit generated html link in terminal and follow steps on page

<p align="center"> Current State of User Interface </p>

![Current User Interface](/img/race_classifier_html.png)

![Current User Interface](/img/race_predict_html.png)


### IN PROGRESS
1. Better UI
2. Deployment (updates to come to this README.md)


## Relevant Info
Note: Inspiration and Data Processing Strategy referenced from https://towardsdatascience.com/formula-1-race-predictor-5d4bfae887da
