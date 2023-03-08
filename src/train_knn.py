import pandas as pd
from pathlib import Path
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os

cwd = os.getcwd()
p = Path(cwd)
_t = pd.read_csv(p/"data/all_applicant_training_data.csv")
_t = _t[_t['gpa_normalized'].notna()]
_t = _t[_t['qs_ranking'].notna()]

train_df = _t[['gpa_normalized', 'is_chinese_undergrad', 'is_985', 'is_211',
               'is_zhuanke', 'is_minban', 'is_heban', 'is_top_100_qs']]
model = NearestNeighbors()
model.fit(train_df)

def _inference(featurized_data: list):
    return model.kneighbors(np.array(featurized_data).reshape(1, -1) , n_neighbors=12)[1] 


def _get_ranges(rankings):
    top_3 = rankings[:3]
    bottom_3 = rankings[-3:]
    middle = rankings[3:-3]
    
    top_3_avg = np.mean(top_3)
    bottom_3_avg = np.mean(bottom_3)
    middle_avg = np.mean(middle)

    top_ranges = (top_3_avg - 20, top_3_avg + 20)
    middle_ranges = (middle_avg - 20, middle_avg + 20)
    bottom_ranges = (bottom_3_avg - 20, bottom_3_avg + 20)
    return top_ranges, middle_ranges, bottom_ranges


def predict_qs_ranking_ranges(featurized_data: list):
    neighbors = _inference(featurized_data)
    rankings = []
    rankings = _t.iloc[neighbors[0]]['qs_ranking'].dropna().to_list()
    rankings.sort()
    return _get_ranges(rankings)