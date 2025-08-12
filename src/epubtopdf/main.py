#!/usr/bin/env python3
"""Main entry point for EPUB to PDF Converter application.

This module provides both command-line and GUI interfaces for converting
EPUB files to PDF format.
"""

import sys
import argparse
from pathlib import Path

from .converter import EpubToPdfConverter, ConversionError
from .gui import EpubToPdfGUI


def create_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Convert EPUB files to PDF format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s book.epub                    # Convert to book.pdf (GUI mode)
  %(prog)s book.epub -o output.pdf      # Convert with custom output name
  %(prog)s book.epub --cli              # Command-line mode
  %(prog)s --gui                        # Launch GUI without file
"""
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Input EPUB file to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file path (default: same name as input with .pdf extension)'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Use command-line interface instead of GUI'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch GUI interface (default behavior)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='EPUB to PDF Converter v1.0.0'
    )
    
    return parser


def cli_convert(input_file: str, output_file: str = None) -> bool:
    """Perform conversion using command-line interface."""
    try:
        # Validate input file
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"Error: Input file '{input_file}' does not exist.")
            return False
            
        if not input_path.suffix.lower() == '.epub':
            print(f"Error: Input file must be an EPUB file.")
            return False
            
        # Set output file
        if output_file is None:
            output_file = str(input_path.with_suffix('.pdf'))
            
        output_path = Path(output_file)
        
        # Check if output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Converting '{input_file}' to '{output_file}'...")
        
        # Create converter
        converter = EpubToPdfConverter()
        
        # Set up progress callback
        def progress_callback(progress):
            print(f"Progress: {progress}%")
            
        converter.set_progress_callback(progress_callback)
        
        # Perform conversion
        success = converter.convert(str(input_path), str(output_path))
        
        if success:
            print(f"Conversion completed successfully!")
            print(f"Output saved to: {output_file}")
            return True
        else:
            print("Conversion failed!")
            return False
            
    except ConversionError as e:
        print(f"Conversion error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # If no arguments provided, launch GUI
    if len(sys.argv) == 1:
        try:
            app = EpubToPdfGUI()
            app.run()
        except Exception as e:
            print(f"Failed to start GUI: {e}")
            sys.exit(1)
        return
    
    # If --gui flag is provided, launch GUI
    if args.gui:
        try:
            app = EpubToPdfGUI()
            app.run()
        except Exception as e:
            print(f"Failed to start GUI: {e}")
            sys.exit(1)
        return
    
    # If input file is provided but no --cli flag, launch GUI with file pre-loaded
    if args.input_file and not args.cli:
        try:
            app = EpubToPdfGUI()
            # Pre-load the file (would need to modify GUI class to accept this)
            app.epub_path.set(args.input_file)
            if args.output:
                app.pdf_path.set(args.output)
            app.run()
        except Exception as e:
            print(f"Failed to start GUI: {e}")
            sys.exit(1)
        return
    
    # Command-line mode
    if args.input_file:
        success = cli_convert(args.input_file, args.output)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
