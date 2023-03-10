from fastapi import FastAPI
from src.interface import Major, InputMessage, TieredResult, tier_name_mapping, MajorRequest, MajorResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from src.school_finder import find_majors
from src.school_details import get_school_details
import uvicorn

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.post("/select-majors", response_model=list[TieredResult])
def major_selection(msg: InputMessage):
    majors = find_majors(msg)
    # td = test_data()
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
                      major_id = str(major['id'].iloc[i]))
            major_list.append(m)
        major_list.sort()
        res.append(TieredResult(tierRanking=_, tierName=tier_name_mapping[_], majorList=major_list))
    return res


@app.get("/major_details/{major_id}", response_model=MajorResponse)
def major_details(major_id):
    res = get_school_details(major_id)
    return res

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)