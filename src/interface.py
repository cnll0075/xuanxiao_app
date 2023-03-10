from functools import total_ordering
from pydantic import BaseModel

class Major(BaseModel,):
    schoolName: str
    schoolEnglishName: str
    specializedSubject: str
    region: str
    qsRanking: str
    qsRanking_top_100: bool
    major_id: str

    @total_ordering
    def __lt__(self, other):
        return int(self.qsRanking) < int(other.qsRanking)


class TieredResult(BaseModel):
    tierRanking: int
    tierName: str
    majorList: list[Major]

tier_name_mapping = {0: '冲刺学校', 1: '安全学校', 2: '保底学校'}

class InputMessage(BaseModel):
    applicantUndergrad: str
    applicantMajor: str
    tuitionRange: str
    countryInterested: str
    majorInterested: str
    estimatedEntranceTime: str
    estimatedApplicationTime: str
    highestDegree: str
    GPA: float
    grade: str
    userID: str


class MajorRequest(BaseModel):
    major_id: str


class MajorResponse(BaseModel):
    major: Major
    majorMainSubject: str
    programLength: str
    entranceTime: str
    tuition: str
    toefl: str
    ielts: str
    toeflSub: str
    ieltsSub: str
    curriculum: str
