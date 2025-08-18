import joblib
import numpy as np

saved_model = joblib.load('model.joblib')
print('loaded the model')

def make_prediction(data: dict) -> float:
    features = np.array([
        [
            data['longitude'],
            data['latitude'],
            data['housing_median_age'],
            data['total_rooms'],
            data['total_bedrooms'],
            data['population'],
            data['households'],
            data['median_income']
        ]
    ])
    return float(saved_model.predict(features)[0])