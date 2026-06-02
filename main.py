import streamlit as st
import pdfplumber as pd
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
<style>
            
/* Reduce top spacing */
.block-container {
    padding-top: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white;
}
                        
/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #334155
    );
}

/* Headers */
h1, h2, h3 {
    color: white !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );
    color: white;
    border: none;
}

/* Button hover */
.stButton > button:hover {
    transform: scale(1.02);
}

/* Text area */
textarea {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🚀 CareerPilot AI


### Your AI-Powered Career Growth Platform

Optimize Resumes • Master Interviews • Build Career Roadmaps
""")
st.info(
    "👋 Welcome to CareerPilot AI. Choose a tool from the sidebar to get started."
)

with st.sidebar:

    st.markdown("# 🚀 CareerPilot AI")

    st.markdown("---")

    st.markdown("### 🧠 AI Tools")

    tool = st.radio(
        "",
        [
            "📄 Resume Optimizer",
            "🎤 Interview Assistant",
            "🛣️ Career Path Advisor"
        ]
    )

    st.markdown("---")

    st.markdown("### 📊 Platform Stats")

    st.metric("Tools", "3")
    st.metric("AI Model", "Groq")

    st.markdown("---")

    st.markdown(
        """
        ### 🚀 Career Tip

        Keep your resume to 1–2 pages and quantify achievements whenever possible.
        """
    )

if tool == "📄 Resume Optimizer":
    col1, col2 = st.columns([1, 1])

    
    # LEFT SIDE (INPUT)
    
    with col1:
        st.header("Upload & Details")

        st.info(
            "📄 Upload your PDF resume and paste the target job description."
        )

        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        description = st.text_area("Job Description",placeholder="Paste the complete job description here...")

        sub = st.button("🚀 Optimize Resume")

    
    # RIGHT SIDE (BENTO DASHBOARD)
    
    with col2:
        st.header("AI Dashboard")

        if sub:
            if resume and description:

                # Extract PDF text
                with pd.open(resume) as pdf:
                    resume_text = ""
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            resume_text += text

                # Prompt for Gemini
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
                    {resume_text}

                    Job Description:
                    {description}
                    """

                # AI Call
                try:

                    with st.spinner("🤖 Analyzing Resume..."):
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )

                    result = response.choices[0].message.content
                except Exception as e:

                    st.error(f"AI Service Error: {e}")
                    st.stop()

                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()
                data = json.loads(result)
                ats_score = data["ats_score"]
                match_level = data["match_level"]
                keywords = data["missing_keywords"]
                strengths = data["strengths"]
                suggestions = data["suggestions"]
                summary = data["optimized_summary"]

                # BENTO GRID UI
                # DASHBOARD

                # TOP METRICS
                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric("🎯 ATS Score", f"{ats_score}%")
                    st.progress(ats_score / 100)

                with m2:
                    st.metric("📊 Match Level", match_level)
                    if match_level == "Excellent":
                        st.success("🟢 Excellent Match")
                    elif match_level == "Good":
                        st.info("🔵 Good Match")
                    elif match_level == "Average":
                        st.warning("🟡 Average Match")
                    else:
                        st.error("🔴 Weak Match")
                                    

                with m3:
                    st.metric("🔑 Missing Keywords", len(keywords))


                # ATS STATUS
                if ats_score >= 80:
                    st.success("🟢 Strong ATS Match")
                elif ats_score >= 60:
                    st.warning("🟡 Moderate ATS Match")
                else:
                    st.error("🔴 Needs Improvement")


                st.divider()


                # KEYWORDS + STRENGTHS
                left, right = st.columns(2)

                with left:
                    with st.container(border=True):
                        st.subheader("🔑 Missing Keywords")

                        if keywords:
                            for k in keywords:
                                st.markdown(f"• {k}")
                        else:
                            st.success("No important keywords missing")


                with right:
                    with st.container(border=True):
                        st.subheader("💪 Resume Strengths")

                        if strengths:
                            for s in strengths:
                                st.markdown(f"• {s}")
                        else:
                            st.info("No strengths returned")


                st.divider()


                # SUMMARY CARD
                with st.container(border=True):
                    st.subheader("✨ Optimized Summary")
                    st.write(summary)


                st.divider()


                # SUGGESTIONS CARD
                with st.container(border=True):
                    st.subheader("💡 AI Suggestions")

                    for s in suggestions:
                        st.markdown(f"✅ {s}")
            else:
                st.error("Please upload resume and enter job description")

        else:
            st.info("Upload resume and click optimize to see AI results")
elif tool == "🎤 Interview Assistant":
    st.header("🎤 Interview Assistant")
    role = st.text_input("Job Role")

    experience = st.selectbox(
        "Experience Level",
        ["Fresher", "1-3 Years", "3-5 Years", "5+ Years"]
    )

    generate = st.button("Generate Questions")

    if generate:
        if generate and not role:
            st.warning("⚠️ Please enter a job role.")
            st.stop()
        prompt=f"""
            You are a senior technical interviewer and career coach.

            Generate interview preparation content for:

            Role: {role}
            Experience Level: {experience}

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
        try:
            with st.spinner("🤖 Generating Interview Questions..."):
                response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}])
        except Exception as e:
            st.error(f"AI Service Error: {e}")
            st.stop()
        

        result = response.choices[0].message.content
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        data = json.loads(result)
        tab1, tab2, tab3 = st.tabs(["🧠 Technical", "🤝 Behavioral", "💼 HR"])

        with tab1:
            for q in data["technical"]:
                with st.container(border=True):
                    st.markdown(f"### ❓ {q['question']}")
                    st.write(q["answer"])

        with tab2:
            for q in data["behavioral"]:
                with st.container(border=True):
                    st.markdown(f"### ❓ {q['question']}")
                    st.write(q["answer"])

        with tab3:
            for q in data["hr"]:
                with st.container(border=True):
                    st.markdown(f"### ❓ {q['question']}")
                    st.write(q["answer"])

elif tool == "🛣️ Career Path Advisor":
    st.header("🛣️ Career Path Advisor")
    dream_career = st.text_input("🎯 Enter Your Dream Career",
        placeholder="e.g. AI Engineer, Data Scientist, Full Stack Developer")

    generate = st.button("🚀 Generate Roadmap")

    if generate:
        if not dream_career:
            st.warning("⚠️ Please enter a dream career.")
            st.stop()
        prompt= f"""
        You are an expert Career Coach.

        Create a roadmap for becoming a:

        {dream_career}

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
        try:
                
            with st.spinner("🧠 Generating Career Roadmap..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}])
        except Exception as e:
            st.error(f"AI Service Error: {e}")
            st.stop()
        

        result = response.choices[0].message.content

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        data = json.loads(result)

        tab1,tab2,tab3,tab4= st.tabs( ["🛣️ Roadmap", "🛠️ Skills", "💻 Projects", "💡 Tips"])

        with tab1:
            for step in data["roadmap"]:
                with st.container(border=True):
                    st.write(f"🚀 {step}")

        with tab2:
            for skill in data["skills"]:
                st.success(f"✅ {skill}")

        with tab3:
            for project in data["projects"]:
                with st.container(border=True):
                    st.write(f"💻 {project}")

        with tab4:
            for tip in data["tips"]:
                st.warning(f"💡 {tip}")

        st.success(f"🎯 Roadmap Generated for: {dream_career}")