from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from textblob import TextBlob
import io
import re
from collections import Counter

app = FastAPI()

# Allow frontend access later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def summarize_text(text, max_sentences=3):
    sentences = text.split(".")
    return ".".join(sentences[:max_sentences]) + "."

def extract_keywords(text, top_n=5):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    common_words = Counter(words).most_common(top_n)
    return [word for word, count in common_words]

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(contents)
    else:
        text = contents.decode("utf-8")

    if not text.strip():
        return {"error": "No readable text found."}

    summary = summarize_text(text)
    sentiment = TextBlob(text).sentiment.polarity

    if sentiment > 0:
        mood = "Positive"
    elif sentiment < 0:
        mood = "Negative"
    else:
        mood = "Neutral"

    keywords = extract_keywords(text)

    return {
        "filename": file.filename,
        "summary": summary,
        "sentiment_score": sentiment,
        "sentiment_label": mood,
        "keywords": keywords
    }