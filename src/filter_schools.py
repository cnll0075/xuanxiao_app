import pandas as pd
from src.interface import InputMessage
from pathlib import Path
import os


region_map = {"澳洲": 'Australia', 
              '英国': 'Britain', 
              '新加坡': 'Singapore', 
              '美国': 'US',
              '中国香港': 'HongKong'}

major_map = {"商科": "商科", 
             "工程" : "工科", 
             "教育" : ["教育"],
             "计算机" :["计算机"],
             "传媒": ["传播", "文化", "影视"],
             "人文社科": ["社科"],
             "法学": ["法律"],
             "医学": ["医学", "公共卫生"],
             "其他": ["数学", "生物", "化学", "生物工程", "物理", "地球科学"] }

tuition_map = {"10万/年以下": [0,100000],
               "10~25万/年": [100000, 250000],
               "10～25万/年": [100000, 250000],
               "25~40万/年": [250000, 400000],
               "25～40万/年": [250000, 400000],
               "40万/年以上": [400000, 800000],
               "没有想好": [0, 800000]}

cwd = os.getcwd()
p = Path(cwd)
all_majors = pd.read_csv(p/"data/指南者专业信息全.csv")

def _filter_school_by_region_and_major(msg: InputMessage, df):
    country = msg.countryInterested
    region = region_map[country]

    major = msg.majorInterested
    mapped_major = major_map[major]

    if isinstance(mapped_major, str):
        _df = df[(df['region'] == region) & (df['major_area'] == mapped_major)]
    else: # a list
        _df = df[(df['region'] == region)]
        _df = _df[_df['area_1'].isin(mapped_major)]
    
    return _df

def _filter_school_by_tuition(msg: InputMessage, df):
    tuition_budget = msg.tuitionRange
    tuition_range = tuition_map[tuition_budget]
    _df = df[(df['tuition_cny'] < tuition_range[1]) & (df['tuition_cny'] > tuition_range[0])]
    return _df


def filter_schools(msg: InputMessage):
    _df = _filter_school_by_region_and_major(msg, all_majors)
    _df = _filter_school_by_tuition(msg, _df)
    return _df