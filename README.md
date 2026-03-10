# PDF AI Analyzer

A web application that analyzes PDF documents using AI to generate summaries and key insights.

## Features

- 📄 PDF text extraction using PyMuPDF
- 🤖 AI-powered document analysis
- 📊 Summary generation
- 💡 Key insights extraction
- 🌐 Clean web interface
- 🚀 Fast and efficient processing

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **PDF Processing**: PyMuPDF (fitz)
- **AI Integration**: OpenAI-compatible API

## Project Structure

```
cloudinsight/
│
├── app/
│   ├── main.py              # FastAPI application
│   ├── pdf_processor.py     # PDF text extraction
│   ├── ai_analyzer.py       # AI integration
│   └── schemas.py           # Data models
│
├── routers/
│   └── analyze.py           # API endpoints
│
├── templates/
│   └── index.html           # Frontend UI
│
├── static/
│   └── script.js            # Frontend logic
│
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

### 1. Clone or navigate to the project directory

```bash
cd "/Users/pranesh/Devloper/Cloud Product/cloudinsight"
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Set up AI API credentials

The application uses an OpenAI-compatible API for document analysis. You can configure it using environment variables:

```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_API_URL="https://api.openai.com/v1/chat/completions"  # Optional
```

**Note**: If you don't have an API key, the application will use a fallback analysis mode that provides basic statistics instead of AI-powered insights.

## Running the Application

### Start the server

```bash
uvicorn main:app --reload
```

The application will be available at: **http://127.0.0.1:8000**

### Access the web interface

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## Usage

1. **Upload PDF**: Click the upload area or drag and drop a PDF file (max 10MB)
2. **Analyze**: Click the "Analyze Document" button
3. **View Results**: See the AI-generated summary and key insights
4. **Analyze More**: Click "Analyze Another Document" to process a new file

## API Endpoints

### `GET /`
Serves the main web interface

### `POST /api/analyze`
Analyzes an uploaded PDF document

**Request**: Multipart form data with PDF file

**Response**:
```json
{
  "summary": "Document summary...",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ],
  "success": true,
  "message": "Analysis completed successfully"
}
```

### `GET /api/health`
Health check endpoint

### `GET /api/info`
Get API information

## Development

### Run with auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run tests

```bash
# Test the health endpoint
curl http://127.0.0.1:8000/api/health

# Test the API info endpoint
curl http://127.0.0.1:8000/api/info
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: PDF extraction fails

**Solution**: Ensure the PDF contains extractable text (not scanned images). The application works best with text-based PDFs.

### Issue: AI analysis returns fallback results

**Solution**: Check that your `OPENAI_API_KEY` environment variable is set correctly. The application will use basic text statistics if the AI API is unavailable.

### Issue: Port already in use

**Solution**: Use a different port:
```bash
uvicorn main:app --reload --port 8001
```

## Features in Detail

### PDF Processing
- Extracts text from all pages
- Handles multi-page documents efficiently
- Cleans and preprocesses text
- Validates PDF content

### AI Analysis
- Sends extracted text to AI API
- Generates concise summaries
- Extracts 3-5 key insights
- Handles large documents (up to 12,000 characters)
- Fallback mode when AI is unavailable

### Web Interface
- Drag-and-drop file upload
- Real-time progress indicators
- Responsive design
- Error handling and validation
- Beautiful gradient UI

## Future Enhancements

- Support for multiple file formats (DOCX, TXT)
- Batch processing
- Export results to PDF/DOCX
- User authentication
- Document history
- Advanced analytics

## License

This project is for educational purposes (university project demonstration).

## Author

Built as a university project demonstration.

## Support

For issues or questions, please check the troubleshooting section above.
