# Quick Start Guide - PDF AI Analyzer

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
uvicorn main:app --reload
```

### Step 3: Open Your Browser
Navigate to: **http://127.0.0.1:8000**

That's it! You're ready to analyze PDFs.

---

## 📝 How to Use

1. **Upload a PDF**: Drag and drop or click to browse
2. **Click Analyze**: Wait for AI processing (usually 5-10 seconds)
3. **View Results**: See summary and key insights
4. **Analyze More**: Click "Analyze Another Document"

---

## 🔑 Optional: Configure AI API

For AI-powered analysis (recommended):

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Without an API key, the app uses fallback mode with basic statistics.

---

## 🧪 Test the API

Run the test script:
```bash
python test_api.py
```

Test endpoints manually:
- Health: http://127.0.0.1:8000/api/health
- Info: http://127.0.0.1:8000/api/info

---

## 🛠️ Troubleshooting

**Problem**: Module not found errors
**Solution**: `pip install -r requirements.txt`

**Problem**: Port already in use
**Solution**: `uvicorn main:app --reload --port 8001`

**Problem**: PDF extraction fails
**Solution**: Ensure PDF has extractable text (not scanned images)

---

## 📚 Project Files

- `main.py` - FastAPI application
- `app/pdf_processor.py` - PDF text extraction
- `app/ai_analyzer.py` - AI integration
- `routers/analyze.py` - API endpoints
- `templates/index.html` - Web interface
- `static/script.js` - Frontend logic

---

## 💡 Tips

- Maximum PDF size: 10MB
- Works best with text-based PDFs
- Results appear in 5-10 seconds
- Supports multi-page documents
- Clean, modern web interface

---

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Built for university project demonstration**
