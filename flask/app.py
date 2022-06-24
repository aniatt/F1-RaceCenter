from flask import Flask, request, render_template
import pickle

from predict import *
from sentiment import *

app = Flask(__name__)
with open('model/finalized_model.joblib', 'rb') as f: clf = pickle.load(f) 

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    raceYear = request.form["season"]
    roundNum = request.form["round"]
    df = generateDataset(raceYear,roundNum)

    test = df.copy()
    X_test = test.drop(['driver', 'podium'], axis = 1)
    y_test = test[['podium', 'driver']]
    y_test.reset_index(inplace = True, drop = True)
    y_pred = pd.DataFrame(clf.predict_proba(X_test), columns = ['proba_0', 'proba_1'])
    
    prediction_df = pd.merge(y_test, y_pred, left_index = True, right_index = True)
    prediction_df = prediction_df.rename(columns = {'driver': 'Starting Grid'})

    race_classification_df = prediction_df.copy()
    race_classification_df.sort_values('proba_1', ascending = False, inplace = True)
    race_classification_df.reset_index(inplace = True, drop = True)
    race_classification_df = race_classification_df.rename(columns = {'Starting Grid': 'Predicted Finish'})

    startingGrid = prediction_df['Starting Grid']
    predictedClass = race_classification_df['Predicted Finish']
    result = pd.DataFrame(columns = ['Starting Grid', 'Predicted Finish'])
    result['Starting Grid'] = startingGrid
    result['Predicted Finish'] = predictedClass
    result = uniformNames(result)

    # SENTIMENT ANALYSIS
    sentiment = sentimentAnalysis(result)
    result = result.join(sentiment)

    return render_template('index.html', column_names=result.columns.values, row_data=list(result.values.tolist()), zip=zip)

if __name__ == "__main__":
    app.run()