from src.data_processing import featurize
from src.filter_schools import filter_schools, all_majors
from src.train_knn import predict_qs_ranking_ranges
from src.interface import InputMessage
import random
from fuzzywuzzy import fuzz
import pandas as pd

def _find_schools_with_ranking_ranges(candidate_schools, ranges):
    top_schools = candidate_schools[(candidate_schools['qs_ranking'] <= ranges[0][1]) & (candidate_schools['qs_ranking'] >= ranges[0][0]) ]
    middle_schools = candidate_schools[(candidate_schools['qs_ranking'] <= ranges[1][1]) & (candidate_schools['qs_ranking'] >= ranges[1][0]) ]
    bottom_schools = candidate_schools[(candidate_schools['qs_ranking'] <= ranges[2][1]) & (candidate_schools['qs_ranking'] >= ranges[2][0]) ]
    return top_schools, middle_schools, bottom_schools


def _find_majors(undergrad_major: str, schools_df: pd.DataFrame):
    # first select three random schools
    schools = list(schools_df['school_name'].unique())
    if len(schools) > 3:
        schools = random.sample(schools, 3)
        schools_df = schools_df[schools_df['school_name'].isin(schools)]
    
    # then rank the majors by the matching of undergrad_majors
    def _fuzz_matching(m):
        return fuzz.ratio(m, undergrad_major)
    res = []
    for school in schools:
        _t_df = schools_df[schools_df['school_name'] == school]
        if len(_t_df) == 1:
            res.append(_t_df.iloc[0])
        else:
            _t_df['fuzzy_matching_score'] = _t_df['area_1'].apply(_fuzz_matching)
            _t_df = _t_df.sort_values('fuzzy_matching_score', ascending=False)
            res.append(_t_df.iloc[0])
    if len(res) > 0:
        res_df = pd.concat(res, axis=1).T
    else:
        res_df = pd.DataFrame()
    return res_df



def find_schools(msg: InputMessage):
    features: list = featurize(msg)
    predicted_ranges = predict_qs_ranking_ranges(features)
    candidate_school_df = filter_schools(msg)
    candidate_schools = _find_schools_with_ranking_ranges(candidate_school_df, predicted_ranges)
    return candidate_schools


def find_majors(msg: InputMessage):
    candidate_schools = find_schools(msg)
    majors = []
    for schools in candidate_schools:
        majors.append(_find_majors(msg.applicantMajor, schools))
    return majors

