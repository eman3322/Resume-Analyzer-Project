ANALYZE_PROMPT = """You are an expert ATS and resume reviewer.
Compare the RESUME with the JOB DESCRIPTION.

Return ONLY valid JSON in exactly this format, with no extra text and no markdown:
{{
  "match_score": <integer 0-100>,
  "ats_score": <integer 0-100>,
  "missing_keywords": ["..."],
  "strengths": ["..."],
  "weaknesses": ["..."],
  "suggestions": ["..."]
}}

Rules:
- match_score: how well the resume fits this job.
- ats_score: how ATS-friendly the resume is (keywords, clear sections, measurable results, formatting).
- missing_keywords: skills or keywords in the job description that are absent from the resume.
- Each list has at most 8 items. Each item is short, specific and in simple English.
- Be honest. A weak resume must get a low score.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""

REWRITE_PROMPT = """You are a professional resume writer.
Rewrite the resume bullet point below to be stronger:
- Start with a strong action verb.
- Add measurable impact only if it is plausible. Do not invent fake numbers; use placeholders like [X%] if needed.
- Keep it to one line.

Job context (may be empty): {jd}

Bullet: {bullet}

Return ONLY valid JSON, no markdown:
{{"improved": "..."}}
"""

COVER_PROMPT = """Write a {tone} cover letter of at most 250 words for the job below,
using only facts present in the resume. Do not invent experience.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Return ONLY valid JSON, no markdown:
{{"cover_letter": "..."}}
"""

INTERVIEW_PROMPT = """You are an interviewer. Based on the resume and the job description,
generate interview questions.

Return ONLY valid JSON, no markdown, in exactly this format:
{{
  "technical": ["question 1", "question 2", "question 3", "question 4", "question 5"],
  "behavioral": ["question 1", "question 2", "question 3", "question 4", "question 5"]
}}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""