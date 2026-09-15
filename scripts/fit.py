# scripts/fit.py

import os

import joblib
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def fit_model():
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)

    data = pd.read_csv('data/initial_data.csv')

    cat_features = data.select_dtypes(include='object')
    num_features = data.select_dtypes(include=['float'])

    preprocessor = ColumnTransformer(
        [
            (
                'cat',
                OneHotEncoder(
                    drop=params['one_hot_drop'],
                    handle_unknown='ignore'
                ),
                cat_features.columns.tolist()
            ),
            (
                'num',
                StandardScaler(),
                num_features.columns.tolist()
            )
        ],
        remainder='drop',
        verbose_feature_names_out=False
    )

    model = LogisticRegression(
        C=params['C'],
        penalty=params['penalty']
    )

    pipeline = Pipeline(
        [
            ('preprocessor', preprocessor),
            ('model', model)
        ]
    )

    pipeline.fit(
        data,
        data[params['target_col']]
    )

    os.makedirs('models', exist_ok=True)

    with open('models/fitted_model.pkl', 'wb') as fd:
        joblib.dump(pipeline, fd)


if __name__ == '__main__':
    fit_model()