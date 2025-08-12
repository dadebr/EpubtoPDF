"""GUI Module for EPUB to PDF Converter
This module provides a user-friendly graphical interface for converting
EPUB files to PDF format using Tkinter.
"""
import os
import threading
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from .converter import EpubToPdfConverter, ConversionError

class EpubToPdfGUI:
    """Main GUI class for EPUB to PDF converter application."""
    
    def __init__(self):
        self.window = Tk()
        self.window.title("EPUB to PDF Converter v1.0")
        self.window.geometry("600x550")
        self.window.resizable(True, True)
        
        # Initialize converter
        self.converter = EpubToPdfConverter()
        
        # Variables
        self.epub_path = StringVar()
        self.pdf_path = StringVar()
        self.progress_var = IntVar()
        self.status_text = StringVar(value="Ready to convert EPUB files")
        self.tolerant_mode = BooleanVar(value=False)  # New tolerant mode variable
        
        # Create GUI components
        self.create_widgets()
        self.setup_layout()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(W, E, N, S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="EPUB to PDF Converter", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file section
        ttk.Label(main_frame, text="EPUB File:").grid(row=1, column=0, sticky=W, pady=5)
        epub_entry = ttk.Entry(main_frame, textvariable=self.epub_path, width=50)
        epub_entry.grid(row=1, column=1, padx=(10, 5), pady=5, sticky=(W, E))
        ttk.Button(
            main_frame, 
            text="Browse...", 
            command=self.browse_epub_file
        ).grid(row=1, column=2, pady=5)
        
        # Output file section
        ttk.Label(main_frame, text="PDF Output:").grid(row=2, column=0, sticky=W, pady=5)
        pdf_entry = ttk.Entry(main_frame, textvariable=self.pdf_path, width=50)
        pdf_entry.grid(row=2, column=1, padx=(10, 5), pady=5, sticky=(W, E))
        ttk.Button(
            main_frame, 
            text="Browse...", 
            command=self.browse_pdf_file
        ).grid(row=2, column=2, pady=5)
        
        # Tolerant mode checkbox
        self.tolerant_checkbox = ttk.Checkbutton(
            main_frame,
            text="Conversão tolerante (pular elementos problemáticos)",
            variable=self.tolerant_mode
        )
        self.tolerant_checkbox.grid(row=3, column=0, columnspan=3, sticky=W, pady=(10, 5))
        
        # Conversion button
        self.convert_button = ttk.Button(
            main_frame, 
            text="Convert to PDF", 
            command=self.start_conversion
        )
        self.convert_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        ttk.Label(main_frame, text="Progress:").grid(row=5, column=0, sticky=W, pady=5)
        self.progress_bar = ttk.Progressbar(
            main_frame, 
            variable=self.progress_var, 
            maximum=100
        )
        self.progress_bar.grid(row=5, column=1, columnspan=2, sticky=(W, E), padx=(10, 0), pady=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_text, 
            relief=SUNKEN
        )
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=(W, E), pady=(10, 0))
        
        # Log text area
        ttk.Label(main_frame, text="Log:").grid(row=7, column=0, sticky=NW, pady=(10, 5))
        self.log_text = ScrolledText(
            main_frame, 
            height=10, 
            width=70, 
            wrap=WORD
        )
        self.log_text.grid(row=7, column=1, columnspan=2, padx=(10, 0), pady=(10, 0), sticky=(W, E, N, S))
        
        # Configure grid weights for resizing
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
    def setup_layout(self):
        """Set up the layout and styling."""
        # Add some styling
        style = ttk.Style()
        style.theme_use('clam')
        
    def browse_epub_file(self):
        """Open file dialog to select EPUB file."""
        file_path = filedialog.askopenfilename(
            title="Select EPUB File",
            filetypes=[("EPUB files", "*.epub"), ("All files", "*.*")]
        )
        if file_path:
            self.epub_path.set(file_path)
            # Auto-generate PDF filename
            epub_file = Path(file_path)
            pdf_file = epub_file.with_suffix('.pdf')
            self.pdf_path.set(str(pdf_file))
            self.log_message(f"Selected EPUB file: {file_path}")
            
    def browse_pdf_file(self):
        """Open file dialog to select PDF output location."""
        file_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.pdf_path.set(file_path)
            self.log_message(f"PDF output set to: {file_path}")
            
    def log_message(self, message):
        """Add message to log text area."""
        self.log_text.insert(END, f"{message}\n")
        self.log_text.see(END)
        
    def update_progress(self, progress):
        """Update progress bar."""
        self.progress_var.set(progress)
        self.window.update_idletasks()
        
    def update_status(self, status):
        """Update status label."""
        self.status_text.set(status)
        self.window.update_idletasks()
        
    def validate_inputs(self):
        """Validate input fields."""
        epub_file = self.epub_path.get().strip()
        pdf_file = self.pdf_path.get().strip()
        
        if not epub_file:
            messagebox.showerror("Error", "Please select an EPUB file.")
            return False
            
        if not pdf_file:
            messagebox.showerror("Error", "Please specify a PDF output file.")
            return False
            
        if not os.path.exists(epub_file):
            messagebox.showerror("Error", "The selected EPUB file does not exist.")
            return False
            
        # Validate EPUB file
        is_valid, error_msg = self.converter.validate_input(epub_file)
        if not is_valid:
            messagebox.showerror("Error", f"Invalid EPUB file: {error_msg}")
            return False
            
        return True
        
    def start_conversion(self):
        """Start the conversion process in a separate thread."""
        if not self.validate_inputs():
            return
            
        # Disable convert button during conversion
        self.convert_button.config(state='disabled')
        self.progress_var.set(0)
        
        # Set tolerant mode based on checkbox
        tolerant_enabled = self.tolerant_mode.get()
        if tolerant_enabled:
            self.update_status("Starting tolerant conversion...")
            self.log_message("=== Starting Tolerant EPUB to PDF Conversion ===")
            self.log_message("Tolerant mode enabled: problematic elements will be skipped")
        else:
            self.update_status("Starting conversion...")
            self.log_message("=== Starting EPUB to PDF Conversion ===")
        
        # Start conversion in separate thread to prevent GUI freezing
        conversion_thread = threading.Thread(target=self.perform_conversion)
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def show_conversion_results(self, success, skipped_count=0, log_file_path=None):
        """Show conversion results with improved error reporting."""
        if success:
            if skipped_count > 0:
                message = (f"Conversion completed successfully!\n\n"
                          f"Warning: {skipped_count} problematic elements were skipped during conversion.\n"
                          f"For detailed information about skipped elements, check the log file:\n{log_file_path}")
                messagebox.showwarning("Conversion Completed with Warnings", message)
            else:
                messagebox.showinfo("Success", "EPUB file has been successfully converted to PDF!")
        else:
            if self.tolerant_mode.get() and skipped_count > 0:
                message = (f"Conversion failed!\n\n"
                          f"{skipped_count} elements were skipped, but conversion still failed.\n"
                          f"Check the log file for details: {log_file_path}")
            else:
                message = "Conversion failed. Please check the log for details."
            messagebox.showerror("Conversion Failed", message)
        
    def perform_conversion(self):
        """Perform the actual conversion."""
        epub_file = self.epub_path.get().strip()
        pdf_file = self.pdf_path.get().strip()
        
        try:
            # Set progress callback
            self.converter.set_progress_callback(self.update_progress)
            
            # Set tolerant mode in converter
            tolerant_enabled = self.tolerant_mode.get()
            
            # Perform conversion
            self.log_message(f"Converting '{epub_file}' to '{pdf_file}'...")
            if tolerant_enabled:
                self.log_message("Tolerant mode: skipping problematic elements")
            
            # Note: This assumes the converter has been updated to support tolerant mode
            # The converter should return (success, skipped_count, log_file_path)
            if hasattr(self.converter, 'convert_with_tolerant_mode') and tolerant_enabled:
                result = self.converter.convert_with_tolerant_mode(epub_file, pdf_file)
                if isinstance(result, tuple) and len(result) == 3:
                    success, skipped_count, log_file_path = result
                else:
                    success = result
                    skipped_count = 0
                    log_file_path = None
            else:
                success = self.converter.convert(epub_file, pdf_file)
                skipped_count = 0
                log_file_path = None
                
            # Update status and show results
            if success:
                if skipped_count > 0:
                    self.log_message(f"Conversion completed with {skipped_count} elements skipped!")
                    self.update_status(f"Conversion completed with {skipped_count} warnings!")
                else:
                    self.log_message("Conversion completed successfully!")
                    self.update_status("Conversion completed successfully!")
            else:
                self.log_message("Conversion failed!")
                self.update_status("Conversion failed!")
                
            # Show detailed results dialog
            self.show_conversion_results(success, skipped_count, log_file_path)
                
        except ConversionError as e:
            error_msg = str(e)
            self.log_message(f"Conversion error: {error_msg}")
            self.update_status(f"Error: {error_msg}")
            messagebox.showerror("Conversion Error", error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.log_message(error_msg)
            self.update_status(error_msg)
            messagebox.showerror("Error", error_msg)
            
        finally:
            # Re-enable convert button
            self.convert_button.config(state='normal')
            
    def run(self):
        """Start the GUI application."""
        self.log_message("EPUB to PDF Converter v1.0 initialized")
        self.log_message("Select an EPUB file to begin conversion")
        self.window.mainloop()

def main():
    """Entry point for the GUI application."""
    try:
        app = EpubToPdfGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()
