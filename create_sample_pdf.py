"""
Sample PDF Creator for Testing
Creates a simple test PDF to demonstrate the analyzer
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    def create_sample_pdf():
        """Create a sample PDF for testing"""
        filename = "sample_document.pdf"
        
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, height - 100, "Sample Document")
        
        # Content
        c.setFont("Helvetica", 12)
        y_position = height - 150
        
        paragraphs = [
            "This is a sample document created for testing the PDF AI Analyzer.",
            "",
            "The document contains multiple paragraphs with different topics.",
            "It demonstrates how the analyzer extracts text from PDF files.",
            "",
            "Key Features:",
            "1. The analyzer can process multi-page documents",
            "2. It extracts text accurately from PDF format",
            "3. AI generates summaries and key insights",
            "4. The web interface displays results beautifully",
            "",
            "This technology can be used for various applications:",
            "- Document summarization for quick review",
            "- Key information extraction from reports",
            "- Content analysis for research papers",
            "- Automated document processing workflows",
            "",
            "The system uses PyMuPDF for text extraction and integrates",
            "with AI APIs to provide intelligent analysis of document content.",
            "This makes it a powerful tool for document management.",
        ]
        
        for para in paragraphs:
            if para:
                c.drawString(100, y_position, para)
            y_position -= 20
        
        c.save()
        print(f"✅ Created {filename}")
        print(f"📄 You can now upload this file to test the analyzer")
        print(f"🌐 Open http://127.0.0.1:8000 and upload {filename}")
    
    if __name__ == "__main__":
        create_sample_pdf()

except ImportError:
    print("ℹ️  ReportLab not installed.")
    print("")
    print("To create a sample PDF, you can:")
    print("1. Install ReportLab: pip install reportlab")
    print("2. Run this script again: python create_sample_pdf.py")
    print("")
    print("Or simply use any existing PDF file to test the analyzer.")
