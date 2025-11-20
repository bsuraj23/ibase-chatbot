"""PDF Processing Module for Ibase Chatbot."""

import fitz  # PyMuPDF
import pdfplumber
from typing import List, Dict
import os

class PDFProcessor:
    """Handle PDF text extraction and processing."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_pymupdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        text = ""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            raise Exception(f"Error extracting text with PyMuPDF: {str(e)}")
        return text
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """
        Extract text from PDF using pdfplumber (better for tables).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise Exception(f"Error extracting text with pdfplumber: {str(e)}")
        return text
    
    def chunk_text(self, text: str) -> List[Dict]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "text": chunk_text,
                "chunk_index": len(chunks),
                "start_char": i,
                "word_count": len(chunk_words)
            })
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """
        Complete PDF processing pipeline.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text and chunks
        """
        # Extract text (try PyMuPDF first, fallback to pdfplumber)
        try:
            text = self.extract_text_pymupdf(pdf_path)
        except:
            text = self.extract_text_pdfplumber(pdf_path)
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        return {
            "filename": os.path.basename(pdf_path),
            "full_text": text,
            "chunks": chunks,
            "total_chunks": len(chunks),
            "total_chars": len(text)
        }

# Example usage
if __name__ == "__main__":
    processor = PDFProcessor(chunk_size=500, chunk_overlap=100)
    result = processor.process_pdf("sample.pdf")
    print(f"Processed {result['total_chunks']} chunks from {result['filename']}")
