from src.interface import InputMessage
import pandas as pd
import pickle
from pathlib import Path
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os

cwd = os.getcwd()
p = Path(cwd)
with open(p/'data/211.pickle', 'rb') as f:
    school_211 = pickle.load(f)

with open(p/'data/985.pickle', 'rb') as f:
    school_985 = pickle.load(f)

with open(p/'data/chinese_schools.pickle', 'rb') as f:
    chinese_schools = pickle.load(f)

with open(p/'data/zhuanke_schools.pickle', 'rb') as f:
    zhuanke_schools = pickle.load(f)

with open(p/'data/minban_schools.pickle', 'rb') as f:
    minban_schools = pickle.load(f)

with open(p/'data/heban_schools.pickle', 'rb') as f:
    heban_schools = pickle.load(f)

with open('data/top_qs_100_schools.pickle', 'rb') as f:
    top_qs_100_schools = pickle.load(f)

GPA_MEAN = 84.94
GPA_STD = 6.20


def _transform_gpa(gpa):
    try:
        gpa = float(gpa)
        if gpa <= 5:
            gpa = (gpa + 1) * 20
        gpa = (gpa - GPA_MEAN) / GPA_STD
        return gpa
    except Exception as e:
        return GPA_MEAN


def _match_school(school: str, school_list: list):
    if school in school_list:
        return 1
    for s in school_list:
        if fuzz.partial_ratio(school, s) >= 90:
            return 1
    return 0


def featurize(msg: InputMessage):
    gpa = _transform_gpa(msg.GPA)
    is_chn_undergrad = _match_school(msg.applicantUndergrad, chinese_schools)
    is_985 = _match_school(msg.applicantUndergrad, school_985)
    is_211 = _match_school(msg.applicantUndergrad, school_211)
    is_zhuanke = _match_school(msg.applicantUndergrad, zhuanke_schools)
    is_minban = _match_school(msg.applicantUndergrad, minban_schools)
    is_heban = _match_school(msg.applicantUndergrad, heban_schools)
    is_qs_100 = _match_school(msg.applicantUndergrad, top_qs_100_schools)
    return [gpa, is_chn_undergrad, is_985, is_211, is_zhuanke, is_minban, is_heban, is_qs_100]