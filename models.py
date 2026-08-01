from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    candidate_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    linkedin = Column(String(255))
    github = Column(String(255))
    portfolio = Column(String(255))

    company_name = Column(String(255))
    job_title = Column(String(255))
    job_description = Column(Text)

    education = Column(Text)
    experience = Column(Text)
    projects = Column(Text)
    certifications = Column(Text)
    achievements = Column(Text)
    languages = Column(Text)

    required_skills = Column(Text)
    candidate_skills = Column(Text)
    matched_skills = Column(Text)
    missing_skills = Column(Text)
    extra_skills = Column(Text)
    resume_text = Column(Text)

    resume_score = Column(Float)
    resume_percentage = Column(Float)
    job_match_percentage = Column(Float)
    ats_score = Column(Float)

    semantic_score = Column(Float)
    recommendation = Column(String(100))
    explanation = Column(Text)

    status = Column(String(50))


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    job_id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(255))

    job_title = Column(String(255))

    job_description = Column(Text)

class MatchResult(Base):
    __tablename__ = "match_results"

    match_id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer)

    candidate_id = Column(Integer)

    overall_score = Column(Float)

    semantic_score = Column(Float)

    skill_match_score = Column(Float)

    experience_score = Column(Float)

    education_score = Column(Float)

    matched_skills = Column(Text)

    missing_skills = Column(Text)

    explanation = Column(Text)

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    candidate_name = Column(String)

    email = Column(String)

    interview_date = Column(String)

    interview_time = Column(String)

    interview_mode = Column(String)

    status = Column(String, default="Scheduled")