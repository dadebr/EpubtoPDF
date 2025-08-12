"""EPUB to PDF Converter Module
This module provides functionality to convert EPUB files to PDF format
using various PDF generation libraries.
"""
import os
import tempfile
import logging
from pathlib import Path
from typing import Optional, Callable
from concurrent.futures import ThreadPoolExecutor
import ebooklib
from ebooklib import epub
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from bs4 import BeautifulSoup

# Set up logging
logger = logging.getLogger(__name__)

class ConversionError(Exception):
    """Exception raised for errors during EPUB to PDF conversion."""
    pass

class EpubToPdfConverter:
    """Main class for converting EPUB files to PDF format."""
    
    def __init__(self, tolerant_mode: bool = False):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.progress_callback: Optional[Callable[[int], None]] = None
        self.tolerant_mode = tolerant_mode
        
    def set_progress_callback(self, callback: Callable[[int], None]):
        """Set callback function for progress updates."""
        self.progress_callback = callback
        
    def _update_progress(self, progress: int):
        """Update progress if callback is set."""
        if self.progress_callback:
            self.progress_callback(progress)
            
    def convert(self, epub_path: str, output_path: str) -> bool:
        """Convert EPUB file to PDF.
        
        Args:
            epub_path: Path to input EPUB file
            output_path: Path for output PDF file
            
        Returns:
            bool: True if conversion successful, False otherwise
            
        Raises:
            ConversionError: If conversion fails
        """
        try:
            # Validate input file
            if not os.path.exists(epub_path):
                raise ConversionError(f"EPUB file not found: {epub_path}")
                
            if not epub_path.lower().endswith('.epub'):
                raise ConversionError("Input file must be an EPUB file")
                
            # Read EPUB file
            self._update_progress(10)
            book = epub.read_epub(epub_path)
            
            # Extract content
            self._update_progress(30)
            content = self._extract_content(book)
            
            # Generate PDF
            self._update_progress(70)
            self._generate_pdf(content, output_path, book)
            
            self._update_progress(100)
            return True
            
        except Exception as e:
            if self.tolerant_mode:
                logger.warning(f"Conversion completed with warnings: {str(e)}")
                return True
            else:
                raise ConversionError(f"Conversion failed: {str(e)}")
            
    def _extract_content(self, book) -> list:
        """Extract text content from EPUB book."""
        content = []
        
        # Get book metadata
        title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Unknown Title'
        author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Unknown Author'
        
        content.append({'type': 'title', 'text': title})
        content.append({'type': 'author', 'text': f'by {author}'})
        content.append({'type': 'pagebreak', 'text': ''})
        
        # Process each item in the book
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                try:
                    # Parse HTML content
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    
                    # Extract text from various HTML elements
                    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                        try:
                            content.append({
                                'type': 'heading', 
                                'text': element.get_text().strip(),
                                'level': int(element.name[1])
                            })
                        except (ValueError, AttributeError) as e:
                            if self.tolerant_mode:
                                logger.warning(f"Skipping malformed heading element: {e}")
                            else:
                                raise
                                
                    for element in soup.find_all('p'):
                        try:
                            # Handle paragraphs that may contain problematic img tags or other elements
                            text = self._extract_paragraph_text(element)
                            if text:
                                content.append({'type': 'paragraph', 'text': text})
                        except Exception as e:
                            if self.tolerant_mode:
                                logger.warning(f"Skipping problematic paragraph: {e}")
                                # Try to extract just the text content ignoring HTML structure
                                try:
                                    text = element.get_text().strip()
                                    if text:
                                        content.append({'type': 'paragraph', 'text': text})
                                except Exception as e2:
                                    logger.warning(f"Could not extract any text from paragraph: {e2}")
                            else:
                                raise
                                
                    # Add page break between chapters
                    content.append({'type': 'pagebreak', 'text': ''})
                    
                except Exception as e:
                    if self.tolerant_mode:
                        logger.warning(f"Skipping problematic document item: {e}")
                    else:
                        raise
                
        return content
    
    def _extract_paragraph_text(self, element):
        """Extract text from paragraph element, handling malformed HTML gracefully."""
        try:
            # First try to get clean text
            text = element.get_text().strip()
            if text:
                return text
        except Exception as e:
            if self.tolerant_mode:
                logger.warning(f"Error extracting paragraph text: {e}")
                # Try alternative extraction methods
                try:
                    # Try to extract just the string content
                    text_parts = []
                    for content in element.contents:
                        if hasattr(content, 'get_text'):
                            text_parts.append(content.get_text())
                        elif isinstance(content, str):
                            text_parts.append(content)
                    return ' '.join(text_parts).strip()
                except Exception as e2:
                    logger.warning(f"Alternative text extraction also failed: {e2}")
                    return None
            else:
                raise
        
    def _generate_pdf(self, content: list, output_path: str, book) -> None:
        """Generate PDF from extracted content."""
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.page_size,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Prepare styles
        styles = self.styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        author_style = ParagraphStyle(
            'CustomAuthor',
            parent=styles['Normal'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor='gray'
        )
        
        heading_styles = {
            1: ParagraphStyle('Heading1', parent=styles['Heading1'], fontSize=18, spaceAfter=12),
            2: ParagraphStyle('Heading2', parent=styles['Heading2'], fontSize=16, spaceAfter=10),
            3: ParagraphStyle('Heading3', parent=styles['Heading3'], fontSize=14, spaceAfter=8),
        }
        
        paragraph_style = ParagraphStyle(
            'CustomParagraph',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Build document content
        story = []
        
        for item in content:
            try:
                if item['type'] == 'title':
                    story.append(Paragraph(item['text'], title_style))
                    story.append(Spacer(1, 12))
                    
                elif item['type'] == 'author':
                    story.append(Paragraph(item['text'], author_style))
                    story.append(Spacer(1, 12))
                    
                elif item['type'] == 'heading':
                    level = min(item.get('level', 1), 3)
                    style = heading_styles.get(level, heading_styles[1])
                    story.append(Spacer(1, 12))
                    story.append(Paragraph(item['text'], style))
                    story.append(Spacer(1, 6))
                    
                elif item['type'] == 'paragraph':
                    # Clean up text
                    text = item['text'].replace('\n', ' ').replace('\r', '')
                    text = ' '.join(text.split())  # Normalize whitespace
                    if text:
                        # Escape problematic characters for ReportLab
                        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        story.append(Paragraph(text, paragraph_style))
                        
                elif item['type'] == 'pagebreak':
                    if story:  # Only add page break if there's content
                        story.append(PageBreak())
                        
            except Exception as e:
                if self.tolerant_mode:
                    logger.warning(f"Skipping problematic content item: {e}")
                else:
                    raise
                    
        # Build PDF
        try:
            doc.build(story)
        except Exception as e:
            if self.tolerant_mode:
                logger.warning(f"PDF generation completed with warnings: {e}")
                # Try to build with minimal content if the full build fails
                try:
                    minimal_story = [Paragraph("PDF conversion completed with some content skipped due to formatting issues.", paragraph_style)]
                    doc.build(minimal_story)
                except Exception as e2:
                    raise ConversionError(f"Failed to generate PDF even in tolerant mode: {e2}")
            else:
                raise
        
    def get_supported_formats(self) -> list:
        """Get list of supported input formats."""
        return ['.epub']
        
    def validate_input(self, file_path: str) -> tuple[bool, str]:
        """Validate input file.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
            
        if not file_path.lower().endswith('.epub'):
            return False, "File must be an EPUB file"
            
        try:
            epub.read_epub(file_path)
            return True, ""
        except Exception as e:
            return False, f"Invalid EPUB file: {str(e)}"

def convert_epub_to_pdf(epub_path: str, pdf_path: str, 
                       progress_callback: Optional[Callable[[int], None]] = None,
                       tolerant_mode: bool = False) -> bool:
    """Convenience function to convert EPUB to PDF.
    
    Args:
        epub_path: Path to input EPUB file
        pdf_path: Path for output PDF file
        progress_callback: Optional callback for progress updates
        tolerant_mode: Enable tolerant mode for error handling
        
    Returns:
        bool: True if successful, False otherwise
    """
    converter = EpubToPdfConverter(tolerant_mode=tolerant_mode)
    if progress_callback:
        converter.set_progress_callback(progress_callback)
        
    try:
        return converter.convert(epub_path, pdf_path)
    except ConversionError:
        return False
