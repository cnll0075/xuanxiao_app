from src.data_processing import featurize
from src.filter_schools import filter_schools, all_majors
from src.train_knn import predict_qs_ranking_ranges
from src.interface import InputMessage


def _find_schools_with_ranking_ranges(candidate_schools, ranges):
    top_schools = candidate_schools[(candidate_schools['qs_ranking'] <= ranges[0][1]) & (candidate_schools['qs_ranking'] >= ranges[0][0]) ]
    middle_schools = candidate_schools[(candidate_schools['qs_ranking'] <= ranges[1][1]) & (candidate_schools['qs_ranking'] >= ranges[1][0]) ]
    bottom_schools = candidate_schools[(candidate_schools['qs_ranking'] <= ranges[2][1]) & (candidate_schools['qs_ranking'] >= ranges[2][0]) ]
    return top_schools, middle_schools, bottom_schools


# def _find_majors(undergradMajor: str, df):



def find_schools(msg: InputMessage):
    features: list = featurize(msg)
    predicted_ranges = predict_qs_ranking_ranges(features)
    candidate_school_df = filter_schools(msg)
    candidate_schools = _find_schools_with_ranking_ranges(candidate_school_df, predicted_ranges)
    return candidate_schools



