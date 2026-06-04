from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CareerPilot AI Backend Running"}

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
)


class ResumeRequest(BaseModel):
    resume_text: str
    description: str


@app.post("/optimize-resume")
def optimize_resume(req: ResumeRequest):

    prompt = f"""
                    You are an expert ATS Resume Optimizer, Senior Technical Recruiter, and Career Coach.

                    Analyze the resume against the job description and provide a realistic ATS evaluation.

                    IMPORTANT RULES:

                    Return ONLY a valid JSON object.

                    Do NOT:
                    - add explanations
                    - add comments
                    - add markdown
                    - add headings
                    - add notes
                    - add code blocks
                    - add ```json
                    - add ``` markers

                    Your response must start with {{
                    and end with }}

                    SCORING RULES:

                    - ATS score must be between 0 and 100.
                    - Be strict and realistic with scoring.
                    - Consider skills, experience, keywords, responsibilities, education, and relevance.
                    - Do not give high scores unless the resume strongly matches the job description.

                    MATCH LEVEL RULES:

                    Match level must be one of:
                    - Excellent
                    - Good
                    - Average
                    - Weak

                    MISSING KEYWORDS RULES:

                    - Return at most 10 important missing keywords.
                    - Prioritize ATS-relevant skills, tools, technologies, certifications, and responsibilities.

                    STRENGTHS RULES:

                    - Return at most 5 strengths.
                    - Focus on experience, achievements, leadership, technical expertise, and relevant qualifications.

                    SUGGESTIONS RULES:

                    - Return exactly 5 actionable suggestions.
                    - Each suggestion must be under 10 words.
                    - Suggestions should improve ATS score and job relevance.

                    OPTIMIZED SUMMARY RULES:

                    Create a premium recruiter-quality professional summary.

                    The summary must:
                    - Be ATS-friendly.
                    - Be tailored to the job description.
                    - Include years of experience if available.
                    - Include the most relevant skills from the resume.
                    - Include important job-description keywords.
                    - Highlight achievements, leadership, and business impact.
                    - Use professional and action-oriented language.
                    - Avoid generic phrases like "hardworking", "passionate", or "motivated".
                    - Sound like it was written by an experienced recruiter.
                    - Be between 60 and 80 words.

                    Return JSON in EXACTLY this format:

                    {{
                        "ats_score": 0,
                        "match_level": "",
                        "missing_keywords": [],
                        "strengths": [],
                        "suggestions": [],
                        "optimized_summary": ""
                    }}

                    Resume:
                    {req.resume_text}

                    Job Description:
                    {req.description}
                    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    result = result.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(result)
    except:
        return {"raw_output": result}
    


class InterviewRequest(BaseModel):
    role: str
    experience: str

@app.post("/interview-questions")
def questions(req: InterviewRequest):
    prompt = f"""
            You are a senior technical interviewer and career coach.

            Generate interview preparation content for:

            Role: {req.role}
            Experience Level: {req.experience}

            IMPORTANT:

            Return ONLY valid JSON.

            Do NOT return:
            - markdown
            - explanations
            - notes
            - comments
            - code blocks
            - ```json
            - extra text

            Return exactly this format:

            {{
                "technical": [
                    {{
                        "question": "",
                        "answer": ""
                    }}
                ],
                "behavioral": [
                    {{
                        "question": "",
                        "answer": ""
                    }}
                ],
                "hr": [
                    {{
                        "question": "",
                        "answer": ""
                    }}
                ]
            }}

            Rules:

            - Generate exactly 5 technical questions.
            - Generate exactly 3 behavioral questions.
            - Generate exactly 2 HR questions.
            - Every question must have a short answer.
            - Answers should be 2-4 lines.
            - Questions should match the role and experience level.
            - Use professional interview-style questions.

            Return JSON only.
            """
    response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                )
    result = response.choices[0].message.content
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)


class CareerRequest(BaseModel):
    dream_career: str

@app.post("/career-roadmap")
def career_roadmap(req: CareerRequest):
    prompt = f"""
        You are an expert Career Coach.

        Create a roadmap for becoming a:

        {req.dream_career}

        Return ONLY valid JSON.

        Format:

        {{
            "roadmap": [],
            "skills": [],
            "projects": [],
            "tips": []
        }}

        Rules:
        - roadmap should contain 5 steps.
        - skills should contain 10 important skills.
        - projects should contain 5 project ideas.
        - tips should contain 5 career tips.
        - Return JSON only.
        """
    response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                )
    
    result = response.choices[0].message.content
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)