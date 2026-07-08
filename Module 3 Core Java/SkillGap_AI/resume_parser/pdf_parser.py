"""
SkillGap AI - PDF Resume Parser
Extracts raw text from PDF resumes using pdfplumber.
"""

import io
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger("pdf_parser")


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract all text from a PDF file using pdfplumber.
    
    Args:
        file_content: Raw bytes of the PDF file
    
    Returns:
        Extracted text as a single string
    """
    try:
        import pdfplumber
        
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            logger.info(f"PDF has {len(pdf.pages)} pages")
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    logger.debug(f"Page {i+1}: extracted {len(page_text)} characters")
        
        full_text = "\n".join(text_parts)
        logger.info(f"Total extracted text: {len(full_text)} characters")
        return full_text
    
    except ImportError:
        logger.warning("pdfplumber not available, trying PyMuPDF fallback")
        return _extract_with_pymupdf(file_content)
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""


def _extract_with_pymupdf(file_content: bytes) -> str:
    """
    Fallback PDF extraction using PyMuPDF (fitz).
    
    Args:
        file_content: Raw bytes of the PDF file
    
    Returns:
        Extracted text string
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(stream=file_content, filetype="pdf")
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        
        full_text = "\n".join(text_parts)
        logger.info(f"PyMuPDF extracted {len(full_text)} characters")
        return full_text
    
    except ImportError:
        logger.error("Neither pdfplumber nor PyMuPDF is available")
        return ""
    except Exception as e:
        logger.error(f"PyMuPDF extraction error: {e}")
        return ""
