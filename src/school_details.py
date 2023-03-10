from src.interface import MajorRequest, MajorResponse, Major
import os
from pathlib import Path
import pandas as pd

def get_school_details(major_id: str):
    cwd = os.getcwd()
    p = Path(cwd)
    all_majors = pd.read_csv(p/"data/指南者专业信息全.csv")

    major_id = int(major_id)
    major = all_majors[all_majors['id'] == major_id]
    m = Major(schoolName =major['school_name'].iloc[0], 
              schoolEnglishName = major['en_name'].iloc[0], 
              specializedSubject = major['ch_name'].iloc[0], 
              region = major['region'].iloc[0], 
              qsRanking = str(major['qs_ranking'].iloc[0]), 
              qsRanking_top_100 = major['is_qs_top_100'].iloc[0], 
              major_id = str(major['id'].iloc[0]))
    res = MajorResponse(major=m, 
                        majorMainSubject=major['area_1'].iloc[0],
                        programLength=major['project_length'].iloc[0],
                        entranceTime=major['entrance_time'].iloc[0],
                        tuition=major['tuition'].iloc[0],
                        toefl=major['tofel'].iloc[0],
                        ielts=major['ielts'].iloc[0],
                        toeflSub=major['tofel_sub'].iloc[0],
                        ieltsSub=major['ielts_sub'].iloc[0],
                        curriculum=major['curriculum'].iloc[0]
                        )
    return res