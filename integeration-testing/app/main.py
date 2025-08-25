from fastapi import FastAPI
from pydantic import BaseModel
from logic import is_eligible_for_loan

app = FastAPI()

class Applicant(BaseModel):
    income: float
    age : int
    employment_status: str


@app.post("/loan-eligibility")
def is_eligible(applicant : Applicant):
    eligibility = is_eligible_for_loan(
        income=applicant.income,
        age=applicant.age,
        employement_status=applicant.employment_status
    )

    return {"eligible": eligibility}