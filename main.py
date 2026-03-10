from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from routers import analyze


# Initialize FastAPI app
app = FastAPI(
    title="PDF AI Analyzer",
    description="AI-powered PDF document analysis tool",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(analyze.router, prefix="/api", tags=["analysis"])


@app.get("/")
async def home(request: Request):
    """Serve the homepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "name": "PDF AI Analyzer",
        "version": "1.0.0",
        "description": "Upload PDF documents for AI-powered analysis"
    }