import PyPDF2
from io import BytesIO
import logging
from typing import Optional
from django.core.files.uploadedfile import UploadedFile
import tempfile

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.max_pages = 50  # Maximum pages to process
        self.chunk_size = 1000  # Characters per chunk for processing
    
    def extract_text(self, pdf_file: UploadedFile) -> str:
        """Extract text content from uploaded PDF file."""
        try:
            with tempfile.NamedTemporaryFile() as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)
                temp_file.seek(0)
                
                pdf_reader = PyPDF2.PdfReader(temp_file)
                text_content = []
                
                # Limit processing to max_pages
                for page_num in range(min(len(pdf_reader.pages), self.max_pages)):
                    page = pdf_reader.pages[page_num]
                    text_content.append(page.extract_text())
                
                return " ".join(text_content)
                
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise ValueError("Failed to extract text from PDF")

    def chunk_text(self, text: str) -> list:
        """Split text into manageable chunks for processing."""
        return [text[i:i + self.chunk_size] 
                for i in range(0, len(text), self.chunk_size)]

    async def summarize(self, pdf_file: UploadedFile) -> str:
        """Generate a summary of the PDF content."""
        try:
            # Extract text from PDF
            full_text = self.extract_text(pdf_file)
            if not full_text.strip():
                raise ValueError("No text content found in PDF")

            # Chunk the text
            text_chunks = self.chunk_text(full_text)
            
            # Process chunks with AI
            summaries = []
            for chunk in text_chunks:
                response = await chatbot_ai.process_query(
                    f"Please summarize this text concisely: {chunk}",
                    role='student'
                )
                summaries.append(response)
            
            # Combine chunk summaries
            final_summary = " ".join(summaries)
            
            return final_summary
            
        except Exception as e:
            logger.error(f"Error summarizing PDF: {str(e)}")
            raise ValueError("Failed to generate PDF summary")

pdf_processor = PDFProcessor()
