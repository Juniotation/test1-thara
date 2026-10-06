import os
import json
import requests
import pandas as pd

def get_gemini_api_key():
    # Looks for key in Streamlit secrets or environment variables
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "")

def call_gemini_api(prompt_text):
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing! Please set it in your environment or Streamlit secrets.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
        
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

def screen_candidate_agent(candidate_row, job_description):
    prompt = f"""
    You are an expert HR Technology & Talent Acquisition Agent for Thara Energy (an integrated Thai oil and gas company).
    Evaluate the following candidate against the Job Description. Be objective, fair, and blind to demographic bias[cite: 1, 2].

    Job Description:
    {job_description}

    Candidate Profile:
    - Name: {candidate_row['full_name']}
    - Degree: {candidate_row['degree']} ({candidate_row['university']})
    - GPA: {candidate_row['gpa']}
    - Years of Experience: {candidate_row['years_experience']}
    - Key Skills: {candidate_row['key_skills']}
    - Work History / Projects: {candidate_row['work_history']}

    Return a valid JSON object with the following exact keys:
    - "score": integer from 0 to 100 representing overall fit.
    - "match_level": string ("High Match", "Medium Match", or "Low Match").
    - "strengths": list of 2-3 bullet point strings detailing why the candidate fits.
    - "gaps": list of 1-2 bullet point strings or areas missing from requirements.
    - "rationale": a concise, executive-level explanation for the screening decision.
    """
    
    response_json_str = call_gemini_api(prompt)
    return json.loads(response_json_str)

def generate_outreach_agent(candidate_row, evaluation):
    prompt = f"""
    You are an AI Recruitment Assistant at Thara Energy[cite: 1, 2].
    Draft a professional, welcoming interview invitation email for the approved candidate, and create 3 technical/behavioral interview questions for the hiring manager to ask based on their skill gaps.

    Candidate Name: {candidate_row['full_name']}
    Candidate Email: {candidate_row['email']}
    Candidate Strengths: {evaluation.get('strengths', [])}
    Candidate Gaps to probe: {evaluation.get('gaps', [])}

    Return a valid JSON object with exact keys:
    - "email_subject": string subject line.
    - "email_body": string body text of the outreach email.
    - "interview_questions": list of 3 tailored questions addressing their background and gaps.
    """
    
    response_json_str = call_gemini_api(prompt)
    return json.loads(response_json_str)