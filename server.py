from fastapi import FastAPI
from src.interface import Major, InputMessage, TieredResult, tier_name_mapping
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from src.school_finder import find_schools, find_majors
import json
import time
app = FastAPI()
import uvicorn

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.post("/select-majors", response_model=list[TieredResult])
def major_selection(msg: InputMessage):
    majors = find_majors(msg)
    # td = test_data()
    # #print(td[0])
    # time.sleep(1)
    #res = [TieredResult(tierRanking=i, tierName=tier_name_mapping[i], majorList=td[i]) for i in range(3)]
    res = []
    for _, major in enumerate(majors):
        major_list = []
        for i in range(len(major)):
            m = Major(schoolName =major['school_name'].iloc[i], 
                      schoolEnglishName = major['en_name'].iloc[i], 
                      specializedSubject = major['ch_name'].iloc[i], 
                      region = major['region'].iloc[i], 
                      qsRanking = str(major['qs_ranking'].iloc[i]), 
                      qsRanking_top_100 = major['is_qs_top_100'].iloc[i], 
                      major_id = major['url'].iloc[i])
            major_list.append(m)
        major_list.sort()
        res.append(TieredResult(tierRanking=_, tierName=tier_name_mapping[_], majorList=major_list))
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

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)