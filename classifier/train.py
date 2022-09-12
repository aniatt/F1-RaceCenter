import pandas as pd
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


def trainModel(data):
  df = data.copy()
  df.podium = df.podium.map(lambda x: 1 if x == 1 else 0)

  train = df[df.season < 2020]
  X_train = train.drop(['driver', 'podium'], axis = 1)
  y_train = train.podium

  params = {
              'n_estimators':[100, 300],
              'max_depth': [5, 8, 15],
              'min_samples_split': [2, 5, 10, 15],
              'min_samples_leaf': [1, 2, 5, 10] 
           }

  clf = GridSearchCV(estimator=RandomForestClassifier(), param_grid=params)
  clf.fit(X_train, y_train)

  print('Best Parameters Found:\n', clf.best_params_)
  return clf


def main():
  df = pd.read_csv('data/final_df.csv')
  print("TRAINING BEGIN")
  clf = trainModel(df)
  print("TRAINING END")
  filename = 'model/finalized_model.joblib'
  pickle.dump(clf, open(filename, 'wb'))

if __name__ == "__main__":
    main()