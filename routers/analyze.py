from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from pathlib import Path

from app.pdf_processor import PDFProcessor
from app.ai_analyzer import AIAnalyzer
from app.schemas import AnalysisResponse, ErrorResponse


router = APIRouter()

# Initialize processors
pdf_processor = PDFProcessor()
ai_analyzer = AIAnalyzer()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Analyze uploaded PDF document
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        Analysis results with summary and key points
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                success=False,
                message="Only PDF files are allowed"
            ).dict()
        )
    
    # Create temporary file to save upload
    temp_file = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Extract text from PDF
        extracted_text = pdf_processor.extract_text(temp_path)
        
        if not extracted_text:
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    success=False,
                    message="Failed to extract text from PDF. The file might be corrupted or contain only images."
                ).dict()
            )
        
        # Clean the extracted text
        cleaned_text = pdf_processor.clean_text(extracted_text)
        
        if not cleaned_text or len(cleaned_text) < 10:
            return JSONResponse(
                status_code=400,
                content=ErrorResponse(
                    success=False,
                    message="PDF appears to be empty or contains insufficient text."
                ).dict()
            )
        
        # Analyze with AI
        analysis_result = ai_analyzer.analyze_document(cleaned_text)
        
        # Return structured response
        return AnalysisResponse(
            summary=analysis_result.get("summary", "No summary available"),
            key_points=analysis_result.get("key_points", []),
            success=True,
            message="Analysis completed successfully"
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                success=False,
                message=f"Error processing PDF: {str(e)}"
            ).dict()
        )
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PDF AI Analyzer"}
