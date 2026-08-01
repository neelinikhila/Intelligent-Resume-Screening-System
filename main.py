from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
print(models.__file__)
print(models.Resume)


models.Base.metadata.create_all(bind=engine)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from fastapi import FastAPI, UploadFile, File, Form, Request,Query
from fastapi.responses import HTMLResponse,FileResponse,RedirectResponse
from openpyxl import Workbook
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from matcher import ResumeMatcher


import os
import shutil
import zipfile
import tempfile

from parser import ResumeParser
from extractor import ResumeExtractor
from section_parser import SectionParser

#from ai.embedding_manager import EmbeddingManager
from ai.candidate_ranker import CandidateRanker
from ai.ats_calculator import ATSCalculator
from ai.explainability import Explainability
#from ai.recommendation_engine import RecommendationEngine
from email_utils import send_interview_email
from ai.interview_generator import InterviewGenerator

import aiosmtplib
from email.message import EmailMessage

async def send_email(to_email, subject, body):
    message = EmailMessage()
    message["From"] = "YOUR_EMAIL@gmail.com"
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="resume.screening.ai@gmail.com",
        password="wzflpuudakpplcqi",
    )

app = FastAPI()


# -----------------------------
# Templates
# -----------------------------

templates = Jinja2Templates(directory="templates")

# -----------------------------
# Static Files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# -----------------------------
# Upload Folder
# -----------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# -----------------------------
# Objects
# -----------------------------

parser = ResumeParser()

extractor = ResumeExtractor()

section_parser = SectionParser()

matcher = ResumeMatcher()

#ai_matcher = SemanticMatcher()


#skill_classifier = SkillClassifier()

explainability = Explainability()

interview_generator = InterviewGenerator()

# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None
        }
    )
@app.get("/bulk-upload", response_class=HTMLResponse)
def bulk_upload_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="bulk_upload.html",
        context={
            "request": request
        }
    )


@app.post("/bulk-upload", response_class=HTMLResponse)
async def bulk_upload(
    request: Request,
    zip_file: UploadFile = File(...),
    company_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...)
):

    temp_dir = tempfile.mkdtemp()

    zip_path = os.path.join(temp_dir, zip_file.filename)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(zip_file.file, buffer)

    extract_folder = os.path.join(temp_dir, "resumes")
    os.makedirs(extract_folder, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    files = os.listdir(extract_folder)
    print(files)

    for file_name in files:

        if not (
            file_name.endswith(".pdf")
            or file_name.endswith(".docx")
        ):
            continue

        print("Processing :", file_name)

        destination = os.path.join(
            UPLOAD_FOLDER,
            file_name
        )

        shutil.copy(
            os.path.join(extract_folder, file_name),
            destination
        )

        try:
            result = await process_resume(
                destination,
                company_name,
                job_title,
                job_description
          )
            print("Saved:", result["candidate_name"])

        except Exception as e:
            print("ERROR:", e)



    return templates.TemplateResponse(
        request=request,
        name="bulk_upload.html",
        context={
            "request": request,
            "message": f"{len(files)} resumes uploaded successfully."
        }
    )

# -----------------------------
# Upload Resume
# -----------------------------
async def process_resume(
    file_path,
    company_name,
    job_title,
    job_description
):
    resume = parser.parse_resume(file_path)

    text = resume["text"]
    hyperlinks = resume["hyperlinks"]

    import re

    SKILLS = [
        "Python","Java","SQL","Machine Learning","Deep Learning",
        "FastAPI","Docker","HTML","CSS","JavaScript",
        "React","Node.js","PostgreSQL","Git",
        "Leadership","Communication","Teamwork"
    ]

    bert_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
            bert_skills.append(skill)

        

        candidate = extractor.extract_candidate_details(
            text,
            hyperlinks
        )

        sections = section_parser.parse_sections(text)

        result = {}

        matched, total, resume_percentage = matcher.resume_score(
        bert_skills
        )

        required_skills, matched_skills, job_match_percentage = matcher.job_match(
            bert_skills,
            job_description
        )

        missing_skills = matcher.missing_skills(
            bert_skills
        )

        candidate_skills = bert_skills
        extra_skills = []
 
        semantic_score = 75
        recommendation = "⭐⭐⭐ Good Match"

    

        resume_percentage = round(
        resume_percentage,
        2
    )

        ats_score = round(
            (
                resume_percentage * 0.30 +
                job_match_percentage * 0.40 +
                semantic_score * 0.30
            ),
            2
        )

    if ats_score >= 85:
        status = "Selected"

    elif ats_score >= 70:
        status = "Shortlisted"

    else:
        status = "Rejected"

    result = {

    "candidate_name": candidate["candidate_name"],
    "email": candidate["email"],
    "phone": candidate["phone"],
    "linkedin": candidate["linkedin"],
    "github": candidate["github"],
    "portfolio": candidate["portfolio"],

    "education": sections["education"],
    "experience": sections["experience"],
    "projects": sections["projects"],
    "skills": sections["skills"],
    "certifications": sections["certifications"],
    "achievements": sections["achievements"],
    "languages": sections["languages"],

    "candidate_skills": candidate_skills,
    "required_skills": required_skills,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "extra_skills": extra_skills,

    "resume_score": f"{matched}/{total}",
    "resume_percentage": f"{resume_percentage}%",
    "job_match_percentage": f"{job_match_percentage}%",
    "ats_score": f"{ats_score:.2f}%",
    "semantic_score": f"{semantic_score:.2f}%",

    "recommendation": recommendation,
    "status": status
}

    db = SessionLocal()

    new_job = models.JobDescription(
        company_name=company_name,
        job_title=job_title,
        job_description=job_description
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    candidate_skills = [str(skill) for skill in candidate_skills]

    

    new_resume = models.Resume(

        candidate_name=candidate["candidate_name"],
        email=candidate["email"],
        phone=candidate["phone"],
        linkedin=candidate["linkedin"],
        github=candidate["github"],
        portfolio=candidate["portfolio"],

        company_name=company_name,
        job_title=job_title,
        job_description=job_description,

        education="\n".join(sections["education"]),
        experience="\n".join(sections["experience"]),
        projects="\n".join(sections["projects"]),
        certifications="\n".join(sections["certifications"]),
        achievements="\n".join(sections["achievements"]),
        languages="\n".join(sections["languages"]),

        required_skills=", ".join(required_skills),
        candidate_skills=", ".join(candidate_skills),
        matched_skills=", ".join(matched_skills),
        missing_skills=", ".join(missing_skills),
        extra_skills=", ".join(extra_skills),

        resume_text=text,

        resume_score=float(resume_percentage),
        resume_percentage=float(resume_percentage),
        job_match_percentage=float(job_match_percentage),
        ats_score=float(ats_score),

        semantic_score=float(semantic_score),
        recommendation=recommendation,

        status=status
        )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    await send_email(
        to_email=new_resume.email,
        subject="Resume Received Successfully",
        body=f"""
    Hi {new_resume.candidate_name},

    Your resume has been received successfully.

    ATS Score: {new_resume.ats_score}%
    Semantic Score: {new_resume.semantic_score}%
    Status: {new_resume.status}

    Thank you for applying.

    Regards,
    HR Team
    """
   )

    new_match = models.MatchResult(
        job_id=new_job.job_id,
        candidate_id=new_resume.id,
        overall_score=float(ats_score),
        semantic_score=float(semantic_score),
        skill_match_score=float(job_match_percentage),
        experience_score=0.0,
        education_score=0.0,
        matched_skills=", ".join(matched_skills),
        missing_skills=", ".join(missing_skills),
        explanation=recommendation
    )

    db.add(new_match)
    db.commit()
    db.close()
    result["bert_skills"] = bert_skills

    return result
@app.post("/upload", response_class=HTMLResponse)

async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    company_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...)
):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

        result = await process_resume(
        file_path,
        company_name,
        job_title,
        job_description
    )

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "result": result
        }
    )

    

        
       

@app.get("/history")
def history(
    request: Request,
    search: str = Query(default=""),
    status: str = Query(default=""),
    sort: str = Query(default="")
):

    db = SessionLocal()

    query = db.query(models.Resume)

    if search:
        query = query.filter(
        (models.Resume.candidate_name.ilike(f"%{search}%")) |
        (models.Resume.email.ilike(f"%{search}%")) |
        (models.Resume.company_name.ilike(f"%{search}%"))
    )

    if status:
        query = query.filter(models.Resume.status == status)

    if sort == "ats":
        query = query.order_by(models.Resume.ats_score.desc())

    elif sort == "semantic":
        query = query.order_by(models.Resume.semantic_score.desc())

    elif sort == "resume":
        query = query.order_by(models.Resume.resume_percentage.desc())

    else:
        query = query.order_by(models.Resume.ats_score.desc())

    resumes = query.all()

    labels = [r.candidate_name for r in resumes]
    ats_scores = [float(r.ats_score or 0) for r in resumes]
    semantic_scores = [float(r.semantic_score or 0) for r in resumes]

    total_resumes = len(resumes)

    selected = len([r for r in resumes if r.status == "Selected"])
    shortlisted = len([r for r in resumes if r.status == "Shortlisted"])
    rejected = len([r for r in resumes if r.status == "Rejected"])

    average_ats = round(
        sum(float(r.ats_score or 0) for r in resumes) / total_resumes,
        2
    ) if total_resumes > 0 else 0

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "resumes": resumes,
            "total_resumes": total_resumes,
            "selected": selected,
            "shortlisted": shortlisted,
            "rejected": rejected,
            "average_ats": average_ats,
            "labels": labels,
            "ats_scores": ats_scores,
            "semantic_scores": semantic_scores,
    }
    )

@app.get("/candidate/{resume_id}", response_class=HTMLResponse)
def candidate_details(resume_id: int, request: Request):

    db = SessionLocal()

    resume = db.query(models.Resume).filter(
        models.Resume.id == resume_id
    ).first()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="candidate.html",
        context={
            "request": request,
            "resume": resume
        }
    )

@app.get("/export/excel")
def export_excel():

    db = SessionLocal()

    resumes = db.query(models.Resume).all()

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Resume History"

    sheet.append([
        "ID",
        "Candidate",
        "Email",
        "Company",
        "Job Title",
        "Resume %",
        "ATS",
        "Semantic",
        "Status"
    ])

    for r in resumes:
        sheet.append([
            r.id,
            r.candidate_name,
            r.email,
            r.company_name,
            r.job_title,
            r.resume_percentage,
            r.ats_score,
            r.semantic_score,
            r.status
        ])

    db.close()

    file_name = "resume_history.xlsx"

    workbook.save(file_name)

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/export/pdf")
def export_pdf():

    db = SessionLocal()

    resumes = db.query(models.Resume).all()

    pdf = SimpleDocTemplate("resume_history.pdf")

    data = [
        ["ID", "Candidate", "ATS", "Semantic", "Status"]
    ]

    for r in resumes:
        data.append([
            r.id,
            r.candidate_name,
            r.ats_score,
            r.semantic_score,
            r.status
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
    ]))

    pdf.build([table])

    db.close()

    return FileResponse(
        path="resume_history.pdf",
        filename="resume_history.pdf",
        media_type="application/pdf"
    )



@app.get("/test-email")
async def test_email():
    await send_email(
        to_email="saisreeadimulam2006@gmail.com",
        subject="Resume Screening System",
        body="Congratulations! Email is working successfully."
    )
    return {"message": "Email sent successfully"}

@app.post("/update_status/{resume_id}")
async def update_status(resume_id: int, status: str = Form(...)):
    db = SessionLocal()

    resume = db.query(models.Resume).filter(
        models.Resume.id == resume_id
    ).first()

    if resume:
        resume.status = status
        db.commit()

        await send_email(
    to_email=resume.email,
    subject="Application Status Updated",
    body=f"""
        Hi {resume.candidate_name},

        Your application status has been updated.

        Status: {resume.status}

        Thank you.

        HR Team
        """
        )

    db.close()

    return RedirectResponse(
        url="/history",
        status_code=303
    )

@app.get("/job/add", response_class=HTMLResponse)
def add_job_page(request: Request):
   return templates.TemplateResponse(
    request=request,
    name="job_description.html",
    context={
        "request": request
    }
)

@app.post("/job/add")
def add_job(
    request: Request,
    company_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...)
):
    db = SessionLocal()

    job = models.JobDescription(
        company_name=company_name,
        job_title=job_title,
        job_description=job_description
    )

    db.add(job)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/job/add",
        status_code=303
    )

@app.get("/jobs", response_class=HTMLResponse)
def view_jobs(request: Request):

    db = SessionLocal()

    jobs = db.query(models.JobDescription).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "request": request,
            "jobs": jobs
        }
    )

@app.get("/match/{job_id}", response_class=HTMLResponse)
def match_resumes(job_id: int, request: Request):

    db = SessionLocal()

    job = db.query(models.JobDescription).filter(
        models.JobDescription.job_id == job_id
    ).first()

    if job is None:
        db.close()
        return HTMLResponse("Job not found", status_code=404)

    resumes = db.query(models.Resume).all()

    matcher = ResumeMatcher() 
    print("Matching started...")
    for resume in resumes:
        print("Matching :", resume.candidate_name)
        if not resume.resume_text:
            continue

        found_skills = skill_classifier.extract_skills(resume.resume_text)

        matched, total, resume_percentage = matcher.resume_score(found_skills)

        jd_skills, matched_skills, keyword_score = matcher.job_match(
            found_skills,
            job.job_description
     )

    
        semantic_score = ai_matcher.semantic_similarity(
        resume.resume_text,
        job.job_description
        )
        missing_skills = matcher.missing_skills(found_skills)

        ats = matcher.ats_score(
            resume_percentage,
            semantic_score
        )

        if ats >= 70:
            status = "Shortlisted"
        else:
            status = "Rejected"
        recommendation = matcher.recommendation(
            ats,
            semantic_score
        )

        explanation = "\n".join(
            explainability.generate(
                matched_skills,
                missing_skills,
                resume_percentage,
                semantic_score,
                ats,
                recommendation
          )
  )

        resume.resume_percentage = resume_percentage
        resume.semantic_score = semantic_score
        resume.ats_score = ats
       
        resume.matched_skills = ", ".join(matched_skills)

        resume.missing_skills = ", ".join(missing_skills)

        resume.recommendation = recommendation

        resume.explanation = explanation

        resume.status = status
        ranker = CandidateRanker()
        resumes = ranker.rank_candidates(resumes)

    db.commit()

    top_candidate = None

    if len(resumes) > 0:
        top_candidate = resumes[0]   

    db.commit()

    response = templates.TemplateResponse(
        request=request,
        name="match_results.html",
        context={
            "request": request,
            "job": job,
            "resumes": resumes,
            "top_candidate": top_candidate
       }
   )

    db.close()

    return response

@app.get("/shortlisted", response_class=HTMLResponse)
def shortlisted_candidates(request: Request):

    db = SessionLocal()

    shortlisted = (
        db.query(models.Resume)
        .filter(models.Resume.status == "Shortlisted")
        .all()
)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="shortlisted.html",
        context={
            "request": request,
            "candidates": shortlisted
       }
   )

@app.get("/interview", response_class=HTMLResponse)
def interview_page(
    request: Request,
    candidate_id: int = None
    
):
    db = SessionLocal()

    candidate = None
    questions = []

    if candidate_id:
        candidate = db.query(models.Resume).filter(
            models.Resume.id == candidate_id
        ).first()

    if candidate:
        questions = interview_generator.generate_questions(
            candidate.resume_text
       )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="interview.html",
        context={
            "request": request,
            "candidate": candidate,
            "questions": questions ,
        }
    )

@app.post("/interview")
def schedule_interview(
    candidate_name: str = Form(...),
    email: str = Form(...),
    interview_date: str = Form(...),
    interview_time: str = Form(...),
    interview_mode: str = Form(...)
):

    db = SessionLocal()

    interview = models.Interview(
        candidate_name=candidate_name,
        email=email,
        interview_date=interview_date,
        interview_time=interview_time,
        interview_mode=interview_mode
    )

    db.add(interview)
    db.commit()
    send_interview_email(
        receiver_email=email,
        candidate_name=candidate_name,
        interview_date=interview_date,
        interview_time=interview_time,
        interview_mode=interview_mode
    )
    db.close()

    return RedirectResponse(
        url="/interview",
        status_code=303
    )

@app.get("/interviews", response_class=HTMLResponse)
def view_interviews(request: Request):

    db = SessionLocal()

    interviews = db.query(models.Interview).all()

    db.close()
    
    return templates.TemplateResponse(
        request=request,
        name="interviews.html",
        context={
            "request": request,
            "interviews": interviews
    }
)

@app.get("/interview/edit/{id}", response_class=HTMLResponse)
def edit_interview(id: int, request: Request):

    db = SessionLocal()

    interview = db.query(models.Interview).filter(
        models.Interview.id == id
    ).first()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="edit_interview.html",
        context={
            "request": request,
            "interview": interview
        }
    )

@app.post("/interview/edit/{id}")
def update_interview(
    id: int,
    candidate_name: str = Form(...),
    email: str = Form(...),
    interview_date: str = Form(...),
    interview_time: str = Form(...),
    interview_mode: str = Form(...)
):

    db = SessionLocal()

    interview = db.query(models.Interview).filter(
        models.Interview.id == id
    ).first()

    interview.candidate_name = candidate_name
    interview.email = email
    interview.interview_date = interview_date
    interview.interview_time = interview_time
    interview.interview_mode = interview_mode
    db.commit()

    send_interview_email(
        receiver_email=email,
        candidate_name=candidate_name,
        interview_date=interview_date,
        interview_time=interview_time,
        interview_mode=interview_mode
     )

    db.close()

    return RedirectResponse(
        url="/interviews",
        status_code=303
    )

    


@app.get("/interview/delete/{interview_id}")
def delete_interview(interview_id: int):

    db = SessionLocal()

    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id
    ).first()

    if interview:
        db.delete(interview)
        db.commit()

    db.close()

    return RedirectResponse(
        url="/interviews",
        status_code=303
    )

