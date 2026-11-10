import re
from io import BytesIO

SKILLS = [
"python","java","javascript","typescript","c++","c","sql","mysql","postgresql","mongodb",
"html","css","react","next.js","node.js","express","fastapi","flask","django","streamlit",
"pandas","numpy","matplotlib","scikit-learn","tensorflow","pytorch","machine learning",
"deep learning","nlp","natural language processing","generative ai","rag","langchain",
"llm","git","github","docker","aws","azure","gcp","linux","rest api","api","data analysis",
"power bi","tableau","excel","oop","data structures","algorithms","redis","supabase"
]

def extract_resume_text(filename, content):
    ext = filename.lower().rsplit(".", 1)[-1]
    if ext == "txt":
        return content.decode("utf-8", errors="ignore")
    if ext == "pdf":
        import fitz
        doc = fitz.open(stream=content, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    if ext == "docx":
        from docx import Document
        doc = Document(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file format.")

def analyze_resume(text):
    low = text.lower()
    skills = sorted({s for s in SKILLS if re.search(r"(?<![a-z0-9])"+re.escape(s)+r"(?![a-z0-9])", low)})
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phones = re.findall(r"(?:\+?\d[\d\s().-]{8,}\d)", text)
    return {"word_count":len(text.split()),"email":emails[0] if emails else None,
            "phone":phones[0].strip() if phones else None,"skills":skills}
