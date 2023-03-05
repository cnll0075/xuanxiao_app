from fastapi import FastAPI
from src.interface import Major, InputMessage, TieredResult, tier_name_mapping
import json
import time
app = FastAPI()

@app.post("/select-majors", response_model=list[TieredResult])
def code_bot(msg: InputMessage):
    td = test_data()
    #print(td[0])
    time.sleep(1)
    res = [TieredResult(tierRanking=i, tierName=tier_name_mapping[i], majorList=td[i]) for i in range(3)]
    return res


def test_data():
    m1 = Major(schoolName='剑桥大学', 
               schoolEnglishName='Cambridge University', 
               specializedSubject='精算学', 
               region='英国',
               qsRanking=2,
               qsRanking_top_100=True,
               major_id=1)
    m2 = Major(schoolName='牛津大学', 
               schoolEnglishName='Oxford University', 
               specializedSubject='统计科学', 
               region='英国',
               qsRanking=4,
               qsRanking_top_100=True,
               major_id=2)
    m3 = Major(schoolName='帝国理工学院', 
               schoolEnglishName='Imperial College London', 
               specializedSubject='数据科学与机器学习', 
               region='英国',
               qsRanking=6,
               qsRanking_top_100=True,
               major_id=3)
    m4 = Major(schoolName='伦敦大学', 
               schoolEnglishName='University of London', 
               specializedSubject='建筑设计', 
               region='英国',
               qsRanking=8,
               qsRanking_top_100=True,
               major_id=4)
    m5 = Major(schoolName='爱丁堡大学', 
               schoolEnglishName='The University of Edinburgh', 
               specializedSubject='机器人科学', 
               region='英国',
               qsRanking=15,
               qsRanking_top_100=True,
               major_id=6)
    m6 = Major(schoolName='曼彻斯特大学', 
               schoolEnglishName='University of Manchester', 
               specializedSubject='石油工程', 
               region='英国',
               qsRanking=28,
               qsRanking_top_100=True,
               major_id=5)
    m7 = Major(schoolName='布里斯托大学', 
               schoolEnglishName='University of Bristol', 
               specializedSubject='化学', 
               region='英国',
               qsRanking=50,
               qsRanking_top_100=True,
               major_id=7)
    
    m8 = Major(schoolName='利兹大学', 
               schoolEnglishName='University of Leeds', 
               specializedSubject='生物学', 
               region='英国',
               qsRanking=90,
               qsRanking_top_100=True,
               major_id=8)
    
    m9 = Major(schoolName='考文垂大学', 
               schoolEnglishName='Coventry University', 
               specializedSubject='建筑学', 
               region='英国',
               qsRanking=120,
               qsRanking_top_100=False,
               major_id=9)
    return [[m1, m2, m3], [m4, m5, m6], [m7, m8, m9]]
