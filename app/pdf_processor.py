import fitz  # PyMuPDF
from typing import Optional


class PDFProcessor:
    """Handles PDF text extraction using PyMuPDF"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a single string or None if error occurs
        """
        try:
            # Open the PDF
            doc = fitz.open(pdf_path)
            
            # Extract text from all pages
            text_content = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_content.append(text)
            
            # Close the document
            doc.close()
            
            # Combine all pages
            full_text = "\n\n".join(text_content)
            
            return full_text
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and preprocess extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        
        # Join lines with single newline
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove multiple spaces
        cleaned_text = ' '.join(cleaned_text.split())
        
        return cleaned_text
