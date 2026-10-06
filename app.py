import streamlit as st
import pandas as pd
import os
from agents import screen_candidate_agent, generate_outreach_agent

st.set_page_config(
    page_title="Thara Energy - AI Recruiting Portal",
    page_icon="⚡",
    layout="wide"
)

# App Header
st.title("⚡ Thara Energy: Agentic Recruiting Workflow")
st.markdown("**P&O Digital, Data & AI (DDAI) Prototype** | Intelligent Graduate Engineer Screening & Human-in-the-Loop Governance[cite: 1, 2]")
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists("candidates.csv"):
        return pd.read_csv("candidates.csv")
    return pd.DataFrame()

@st.cache_data
def load_jd():
    if os.path.exists("job_description.txt"):
        with open("job_description.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "Job Description not found."

df_candidates = load_data()
job_description = load_jd()

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Candidate Screening & Evaluation", "Recruitment Funnel & Database", "System Architecture & Notes"])

if page == "Candidate Screening & Evaluation":
    st.subheader("🤖 AI Agentic Screening & Human-in-the-Loop Approval")
    
    if df_candidates.empty:
        st.error("candidates.csv not found. Please verify your file setup.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 1. Select Candidate")
            selected_name = st.selectbox("Choose Candidate:", df_candidates['full_name'].tolist())
            candidate_row = df_candidates[df_candidates['full_name'] == selected_name].iloc[0]
            
            st.markdown("**Candidate Summary:**")
            st.write(f"**Degree:** {candidate_row['degree']} ({candidate_row['university']})")
            st.write(f"**GPA:** {candidate_row['gpa']}")
            st.write(f"**Experience:** {candidate_row['years_experience']} yrs")
            st.write(f"**Skills:** {candidate_row['key_skills']}")
            st.write(f"**History:** {candidate_row['work_history']}")
            st.write(f"**Current Status:** `{candidate_row['status']}`")
            
            api_key_input = st.text_input("Gemini API Key (Optional if set in environment):", type="password")
            if api_key_input:
                os.environ["GEMINI_API_KEY"] = api_key_input

            run_screening = st.button("🚀 Run AI Screening Agent", type="primary")

        with col2:
            st.markdown("### 2. AI Evaluation & Explainability Dashboard")
            
            if run_screening:
                with st.spinner("AI Agents analyzing candidate profile against Thara Energy success criteria..."):
                    try:
                        evaluation = screen_candidate_agent(candidate_row, job_description)
                        st.session_state['current_evaluation'] = evaluation
                        st.session_state['evaluated_candidate'] = selected_name
                    except Exception as e:
                        st.error(f"Error running agent: {e}")
                        evaluation = None

            if 'current_evaluation' in st.session_state and st.session_state.get('evaluated_candidate') == selected_name:
                eval_data = st.session_state['current_evaluation']
                
                # Metric badges
                m_col1, m_col2 = st.metric("AI Match Score", f"{eval_data.get('score', 0)} / 100"), st.markdown(f"**Match Tier:** `{eval_data.get('match_level', 'N/A')}`")
                
                st.markdown("#### 🔍 Explainability Rationale")
                st.info(eval_data.get('rationale', 'No rationale provided.'))
                
                s_col1, s_col2 = st.columns(2)
                with s_col1:
                    st.markdown("**Key Strengths:**")
                    for s in eval_data.get('strengths', []):
                        st.markdown(f"- {s}")
                with s_col2:
                    st.markdown("**Skill Gaps / Risks:**")
                    for g in eval_data.get('gaps', []):
                        st.markdown(f"- {g}")
                
                st.markdown("---")
                st.markdown("### 3. Human-in-the-Loop Governance Gate")
                st.markdown("Review the AI assessment above and approve or reject the candidate before automated outreach triggers[cite: 1, 4].")
                
                col_app, col_rej = st.columns(2)
                with col_app:
                    if st.button("✅ Approve for Interview", type="secondary"):
                        with st.spinner("Generating personalized outreach and interview questions..."):
                            try:
                                outreach = generate_outreach_agent(candidate_row, eval_data)
                                st.session_state['outreach'] = outreach
                                st.success("Candidate approved! Outreach package generated.")
                            except Exception as e:
                                st.error(f"Error generating outreach: {e}")
                with col_rej:
                    if st.button("❌ Reject Candidate"):
                        st.warning("Candidate marked as rejected in tracking workflow.")
                
                if 'outreach' in st.session_state:
                    out = st.session_state['outreach']
                    st.markdown("#### 📧 Generated Outreach Email")
                    st.text_input("Subject Line:", value=out.get('email_subject', ''))
                    st.text_area("Email Body:", value=out.get('email_body', ''), height=150)
                    
                    st.markdown("#### 🎯 Tailored Interview Questions for Hiring Manager")
                    for idx, q in enumerate(out.get('interview_questions', []), 1):
                        st.markdown(f"**Q{idx}:** {q}")

elif page == "Recruitment Funnel & Database":
    st.subheader("📊 Thara Energy Recruitment Tracking Funnel")
    st.markdown("Overview of all 20 synthetic candidate profiles loaded in the mock ATS database[cite: 1].")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidates", len(df_candidates))
    col2.metric("Target Graduate Roles", 80)
    col3.metric("Applicant Pool Size", "5,000 (Simulated)")
    
    st.dataframe(df_candidates, use_container_width=True)

elif page == "System Architecture & Notes":
    st.subheader("🏛️ Solution Architecture & Design Notes")
    st.markdown("""
    ### Option B: Agentic Recruiting Workflow for Thara Energy
    - **Problem Solved:** Automates initial CV screening for 5,000 graduate applicants while maintaining rigorous explainability and human oversight[cite: 1, 2].
    - **Agentic Pipeline:**
      1. **Agent 1 (Criteria Extraction):** Parses job profile requirements.
      2. **Agent 2 (Candidate Evaluation & Scoring):** Scores candidates on a 0-100 scale, highlighting strengths, energy transition readiness, and gaps with clear rationales.
      3. **Human-in-the-Loop Gate:** Recruiter reviews scores and approves/rejects before any candidate interaction.
      4. **Agent 3 (Outreach & Interview Builder):** Generates personalized invitation emails and custom technical interview questions.
    - **Tech Stack:** Python, Streamlit, Google Gemini 2.5 Flash API, Pandas, GitHub, Streamlit Cloud[cite: 1, 4].
    """)