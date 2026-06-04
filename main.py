import streamlit as st
import pdfplumber as pd
from openai import OpenAI
import json
from dotenv import load_dotenv
import requests

load_dotenv()


st.set_page_config(page_title="AI Career Assistant", page_icon="📄", layout="wide")
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

st.markdown("""
# 🚀 CareerPilot AI


### Your AI-Powered Career Growth Platform

Optimize Resumes • Master Interviews • Build Career Roadmaps
""")
st.info("👋 Welcome to CareerPilot AI. Choose a tool from the sidebar to get started.")

with st.sidebar:

    st.markdown("# 🚀 CareerPilot AI")

    st.markdown("---")

    st.markdown("### 🧠 AI Tools")

    tool = st.radio(
        "", ["📄 Resume Optimizer", "🎤 Interview Assistant", "🛣️ Career Path Advisor"]
    )

    st.markdown("---")

    st.markdown("### 📊 Platform Stats")

    st.metric("Tools", "3")
    st.metric("AI Model", "Groq")

    st.markdown("---")

    st.markdown("""
        ### 🚀 Career Tip

        Keep your resume to 1–2 pages and quantify achievements whenever possible.
        """)

if tool == "📄 Resume Optimizer":
    col1, col2 = st.columns([1, 1])

    # LEFT SIDE (INPUT)

    with col1:
        st.header("Upload & Details")

        st.info("📄 Upload your PDF resume and paste the target job description.")

        resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        description = st.text_area(
            "Job Description", placeholder="Paste the complete job description here..."
        )

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

                # AI Call
                try:

                    with st.spinner("🤖 Analyzing Resume..."):
                        response = requests.post(
                            "http://localhost:8000/optimize-resume",
                            json={
                                "resume_text": resume_text,
                                "description": description,
                            },
                        )
                except Exception as e:

                    st.error(f"AI Service Error: {e}")
                    st.stop()

                data = response.json()
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
        "Experience Level", ["Fresher", "1-3 Years", "3-5 Years", "5+ Years"]
    )

    generate = st.button("Generate Questions")

    if generate:
        if generate and not role:
            st.warning("⚠️ Please enter a job role.")
            st.stop()
        try:
            with st.spinner("🤖 Generating Interview Questions..."):
                response = requests.post(
                            "http://localhost:8000/interview-questions",
                            json={
                                 "role": role,
                                 "experience": experience
                            },
                        )
               
        except Exception as e:
            st.error(f"AI Service Error: {e}")
            st.stop()

        data = response.json()
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
    dream_career = st.text_input(
        "🎯 Enter Your Dream Career",
        placeholder="e.g. AI Engineer, Data Scientist, Full Stack Developer",
    )

    generate = st.button("🚀 Generate Roadmap")

    if generate:
        if not dream_career:
            st.warning("⚠️ Please enter a dream career.")
            st.stop()
        try:

            with st.spinner("🧠 Generating Career Roadmap..."):
                response = requests.post("http://localhost:8000/career-roadmap",json={
        "dream_career": dream_career
    }
)

        except Exception as e:
            st.error(f"AI Service Error: {e}")
            st.stop()

        data = response.json()

        tab1, tab2, tab3, tab4 = st.tabs(
            ["🛣️ Roadmap", "🛠️ Skills", "💻 Projects", "💡 Tips"]
        )

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
