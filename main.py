from pathlib import Path
from fastapi.responses import FileResponse

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    AnalyzeResponse,
    RewriteRequest, RewriteResponse,
    CoverLetterRequest, CoverLetterResponse,
    InterviewRequest, InterviewResponse,
)
from services.parser import extract_text
from services.llm import call_llm
from services.prompts import (
    ANALYZE_PROMPT, REWRITE_PROMPT, COVER_PROMPT, INTERVIEW_PROMPT,
)

app = FastAPI(title="Resume AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent

MAX_SIZE = 5 * 1024 * 1024  # 5 MB
AI_FAIL_MSG = "AI service abhi kaam nahi kar rahi, dobara try karo"



@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):
    data = await resume.read()

    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File 5MB se badi hai")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description khali hai")

    try:
        text = extract_text(data, resume.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="File read nahi ho payi, shayad corrupt hai")

    if len(text) < 50:
        raise HTTPException(status_code=400, detail="Resume khali ya scanned image lag raha hai")

    prompt = ANALYZE_PROMPT.format(resume=text[:8000], jd=job_description[:4000])

    try:
        result = call_llm(prompt)
    except Exception as e:
        print("LLM error:", e)
        raise HTTPException(status_code=502, detail=AI_FAIL_MSG)

    result["resume_text"] = text
    return AnalyzeResponse(**result)


@app.post("/rewrite-bullet", response_model=RewriteResponse)
def rewrite_bullet(req: RewriteRequest):
    if not req.bullet.strip():
        raise HTTPException(status_code=400, detail="Bullet khali hai")

    prompt = REWRITE_PROMPT.format(bullet=req.bullet, jd=req.job_description[:4000])
    try:
        result = call_llm(prompt)
    except Exception as e:
        print("LLM error:", e)
        raise HTTPException(status_code=502, detail=AI_FAIL_MSG)

    return RewriteResponse(original=req.bullet, improved=result["improved"])


@app.post("/cover-letter", response_model=CoverLetterResponse)
def cover_letter(req: CoverLetterRequest):
    if not req.resume_text.strip() or not req.job_description.strip():
        raise HTTPException(status_code=400, detail="Resume aur job description dono chahiye")

    prompt = COVER_PROMPT.format(
        resume=req.resume_text[:8000],
        jd=req.job_description[:4000],
        tone=req.tone,
    )
    try:
        result = call_llm(prompt)
    except Exception as e:
        print("LLM error:", e)
        raise HTTPException(status_code=502, detail=AI_FAIL_MSG)

    return CoverLetterResponse(cover_letter=result["cover_letter"])


@app.post("/interview-questions", response_model=InterviewResponse)
def interview_questions(req: InterviewRequest):
    if not req.resume_text.strip() or not req.job_description.strip():
        raise HTTPException(status_code=400, detail="Resume aur job description dono chahiye")

    prompt = INTERVIEW_PROMPT.format(
        resume=req.resume_text[:8000],
        jd=req.job_description[:4000],
    )
    try:
        result = call_llm(prompt)
    except Exception as e:
        print("LLM error:", e)
        raise HTTPException(status_code=502, detail=AI_FAIL_MSG)

    return InterviewResponse(**result)