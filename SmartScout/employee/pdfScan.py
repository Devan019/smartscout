import json
import os
import re
import fitz
from docx import Document

def load_skills_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return set(data.get("skills", []))  

skills_db = load_skills_from_json('C:\Major projects\SmartScout\smartscout\static\json\skill.json')

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def extract_skills_brute_force(text):
    words = re.findall(r'[A-Za-z0-9#+-]+', text.lower())
    found_skills = {skill for skill in skills_db if skill.lower() in words}
    return list(found_skills)


def process_resume(file):
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == ".pdf":
        resume_text = extract_text_from_pdf(file)
    elif file_extension == ".docx":
        resume_text = extract_text_from_docx(file)
    else:
        return None  

    return {
        "skills": extract_skills_brute_force(resume_text),
        "contact": re.findall(r'\b\d{10}\b', resume_text),  
        "email": re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text),
        "cpi": extract_cpi(resume_text),
        "university": extract_university(resume_text),
        "main_interest": extract_main_interest(resume_text),
        "experience": extract_experience(resume_text)
    }

# Function to extract CPI/CGPA
def extract_cpi(text):
    cpi_match = re.findall(r'(\b\d\.\d{1,2}\b|\b\d{2}%\b)', text)
    return cpi_match[0] if cpi_match else ""

# Function to extract university
def extract_university(text):
    university_match = re.findall(r'\b(?:University|Institute|College) of [A-Za-z\s]+', text)
    return university_match[0] if university_match else ""

# Function to extract main interest
def extract_main_interest(text):
    interests = ["Web Development", "Machine Learning", "Data Science", "Cybersecurity",
                 "AI", "Cloud Computing", "UI/UX Design", "Blockchain", "DevOps"]
    for interest in interests:
        if interest.lower() in text.lower():
            return interest
    return ""

# Function to extract experience
def extract_experience(text):
    exp_match = re.findall(r'(\b\d+\s*(?:years?|months?)\b)', text)
    return exp_match if exp_match else []



