import os
import time
import joblib
import mlflow

import pandas as pd

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor, AdaBoostRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder 

load_dotenv()

if __name__ == "__main__":

    print("training model...")
    start_time = time.time()

    EXPERIMENT_NAME="my-first-mlflow-experiment"
    mlflow.set_tracking_uri(os.environ["APP_URI"])
    mlflow.sklearn.autolog() 
    mlflow.set_experiment(EXPERIMENT_NAME)
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    df = pd.read_csv("./get_around_pricing_project.csv")

    df.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    target = "rental_price_per_day"

    x = df.drop(target, axis=1)
 
    y = df.loc[:,target]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

    def categorie(x):
        numeric_features = []
        categorical_features = []
        for i,t in x.dtypes.items():
            if ('float' in str(t)) or ('int' in str(t)) :
                numeric_features.append(i)
            else :
                categorical_features.append(i)
        return numeric_features, categorical_features

    numeric_features, categorical_features = categorie(x)

    def pipe(numeric_features, categorical_features, x_train, x_test):
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline(steps=[
            ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore')) 
            ])
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features)
            ])
        
        x_train = preprocessor.fit_transform(x_train)
        x_test = preprocessor.transform(x_test)
        return x_train, x_test
        
    x_train, x_test = pipe(numeric_features, categorical_features, x_train, x_test)

    with mlflow.start_run(experiment_id = experiment.experiment_id):

        model = BaggingRegressor()
        model.fit(x_train, y_train)

        predicted_qualities = model.predict(x_test)
        accuracy = model.score(x_test, y_test)

        print("LogisticRegression model")
        print("Accuracy: {}".format(accuracy))

        mlflow.log_metric("Accuracy", accuracy)
        

   

    #joblib.dump(model, "model.joblib")

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")