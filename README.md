# Thara Energy - AI Recruiting Workflow

P&O Digital, Data & AI (DDAI) Case Assessment

## Overview

An AI-powered recruitment screening prototype for graduate engineer
applicants at Thara Energy.

The application uses Google Gemini to:
- Evaluate candidates against a job description
- Generate an explainable match score
- Identify candidate strengths and skill gaps
- Generate personalized interview invitations
- Generate tailored interview questions

## Tech Stack

- Python
- Streamlit
- Google Gemini 2.5 Flash
- Pandas
- Requests

## Project Structure

- `app.py` - Streamlit web application
- `agents.py` - Gemini AI agent logic
- `candidates.csv` - Synthetic candidate data
- `job_description.txt` - Job description used for screening
- `requirements.txt` - Python dependencies

## How to Run Locally

Install dependencies:

```bash
pip install -r requirements.txt

Run the application:

streamlit run app.py
