from pydantic import BaseModel


class ResumeBase(BaseModel):
    candidate_name: str
    email: str
    phone: str
    linkedin: str
    github: str
    portfolio: str

    education: str
    experience: str
    projects: str
    certifications: str
    achievements: str
    languages: str

    required_skills: str
    candidate_skills: str
    matched_skills: str
    missing_skills: str
    extra_skills: str

    resume_score: float
    resume_percentage: float
    job_match_percentage: float
    ats_score: float

    status: str


class ResumeCreate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int

    class Config:
        from_attributes = True