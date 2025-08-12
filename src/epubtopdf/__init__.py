"""EPUB to PDF Converter Package

A Python package that provides functionality to convert EPUB files to PDF format
with a user-friendly GUI interface.
"""

__version__ = "1.0.0"
__author__ = "EPUB to PDF Converter Team"
__email__ = "contact@epubtopdf.example"
__description__ = "A Python GUI application for converting EPUB files to PDF format"

# Import main modules for easier access
from .converter import EpubToPdfConverter
from .gui import EpubToPdfGUI

__all__ = [
    "EpubToPdfConverter",
    "EpubToPdfGUI",
    "__version__",
]
