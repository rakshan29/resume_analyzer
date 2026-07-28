import streamlit as st
import PyPDF2
from groq import Groq
import json

# -------------------------------------------------

# PAGE CONFIGURATION

# -------------------------------------------------

st.set_page_config(
page_title="Resume Analyzer",
page_icon="📄",
layout="centered"
)

# -------------------------------------------------

# GROQ API SETUP

# Store the API key in .streamlit/secrets.toml

# -------------------------------------------------

client = Groq(
api_key=st.secrets["GROQ_API_KEY"]
)

# -------------------------------------------------

# STREAMLIT USER INTERFACE

# -------------------------------------------------

st.title("📄 AI Resume Analyzer")
st.write(
"Upload your resume and paste a job description "
"to check how well your profile matches the role."
)

uploaded_file = st.file_uploader(
"Upload your Resume",
type=["pdf"]
)

job_description = st.text_area(
"Paste the Job Description",
height=200,
placeholder="Paste the complete job description here..."
)

# -------------------------------------------------

# ANALYZE BUTTON

# -------------------------------------------------

if st.button("🔍 Analyze Resume", use_container_width=True):

```
if uploaded_file is None:
    st.error("Please upload your resume PDF.")

elif not job_description.strip():
    st.error("Please paste the job description.")

else:

    # -----------------------------------------
    # EXTRACT TEXT FROM PDF
    # -----------------------------------------
    try:
        with st.spinner("📄 Reading your resume..."):

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            resume_text = ""

            for page in pdf_reader.pages:
                resume_text += page.extract_text() or ""

            if not resume_text.strip():
                st.error(
                    "No readable text was found in this PDF. "
                    "Please upload a text-based resume PDF."
                )
                st.stop()

    except Exception as e:
        st.error(f"Unable to read the PDF: {e}")
        st.stop()

    # -----------------------------------------
    # SEND RESUME TO GROQ AI
    # -----------------------------------------
    try:
        with st.spinner("🤖 AI is analyzing your resume..."):

            prompt = f"""
```

You are an expert HR recruiter and ATS resume analyzer.

Compare the candidate's resume with the job description.

Give a realistic match score based on:

* Technical skills
* Required qualifications
* Experience
* Relevant projects
* Keywords

Return ONLY valid JSON in this exact format:

{{
"match_percentage": 75,
"missing_skills": [
"Skill 1",
"Skill 2"
],
"matched_skills": [
"Skill 1",
"Skill 2"
],
"summary": "Brief professional advice."
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

```
            chat_completion = (
                client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="openai/gpt-oss-120b",
                    response_format={
                        "type": "json_object"
                    }
                )
            )

            response_text = (
                chat_completion
                .choices[0]
                .message
                .content
            )

            result = json.loads(response_text)

    except json.JSONDecodeError:
        st.error(
            "The AI returned an invalid response. "
            "Please try again."
        )
        st.stop()

    except Exception as e:
        st.error(
            f"An error occurred while analyzing "
            f"the resume: {e}"
        )
        st.stop()

    # -----------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------
    st.success("✅ Resume analysis completed!")

    st.divider()

    match_score = result.get(
        "match_percentage",
        0
    )

    st.metric(
        "Resume Match Score",
        f"{match_score}%"
    )

    st.progress(
        min(
            max(
                int(match_score),
                0
            ),
            100
        )
    )

    st.subheader("✅ Matched Skills")

    matched_skills = result.get(
        "matched_skills",
        []
    )

    if matched_skills:
        st.write(
            ", ".join(matched_skills)
        )
    else:
        st.write(
            "No strong matching skills were identified."
        )

    st.subheader("⚠️ Missing Skills")

    missing_skills = result.get(
        "missing_skills",
        []
    )

    if missing_skills:
        st.write(
            ", ".join(missing_skills)
        )
    else:
        st.success(
            "No major missing skills were identified!"
        )

    st.subheader("💡 AI Recommendation")

    st.info(
        result.get(
            "summary",
            "No recommendation available."
        )
    )
```
