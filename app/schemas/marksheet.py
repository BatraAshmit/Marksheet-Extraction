from pydantic import BaseModel
from typing import List, Optional


class FieldValue(BaseModel):
    value: Optional[str] = None
    confidence: float = 0.0


class CandidateDetails(BaseModel):
    name: FieldValue
    father_or_mother_name: FieldValue
    roll_no: FieldValue
    registration_no: FieldValue
    dob: FieldValue
    exam_year: FieldValue
    board_or_university: FieldValue
    institution: FieldValue


class SubjectMarks(BaseModel):
    subject: FieldValue
    max_marks: FieldValue
    obtained_marks: FieldValue
    grade: Optional[FieldValue] = None


class OverallResult(BaseModel):
    result_or_division: FieldValue


class IssueDetails(BaseModel):
    date: FieldValue
    place: FieldValue


class MarksheetResponse(BaseModel):
    candidate_details: CandidateDetails
    subjects: List[SubjectMarks]
    overall_result: OverallResult
    issue_details: IssueDetails
