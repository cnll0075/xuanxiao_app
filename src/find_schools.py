import pandas as pd
from src.interface import InputMessage
from pathlib import Path


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
             "法学": ["法学"],
             "医学": ["医学", "公共卫生"] }

p = Path('.')
all_majors = pd.read_csv(p/"../data/指南者专业信息全.csv")

def _filter_school_by_region_and_major(msg: InputMessage):
    country = msg.countryInterested
    region = region_map[country]

    major = msg.majorInterested
    mapped_major = major_map[major]

    if isinstance(mapped_major, str):
        _df = all_majors[(all_majors['region'] == region) & (all_majors['major_area'] == mapped_major)]
    else: # a list
        _df = all_majors[(all_majors['region'] == region)]
        _df = _df[_df['area_1'].isin(mapped_major)]
    
    return _df