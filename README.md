# EpubtoPDF

A Python application that provides a graphical user interface (GUI) for converting EPUB files to PDF format.

## Features

- Simple and intuitive GUI interface
- Converts EPUB e-books to PDF format
- Easy-to-use file selection and conversion process
- Tolerant mode for handling problematic EPUB files

## Installation

Clone this repository:

```bash
git clone https://github.com/dadebr/EpubtoPDF.git
cd EpubtoPDF
```

## Instalação do Tk

Este projeto utiliza Tkinter para a interface gráfica. O Tkinter já vem incluído com o Python e **não deve ser instalado via pip**.

### Windows

O Tkinter já vem instalado por padrão com o Python no Windows. Se você instalou o Python através do instalador oficial, o Tkinter estará disponível.

### macOS

O Tkinter já vem incluído com o Python no macOS. Se você instalou o Python através do Homebrew, pode ser necessário instalar o suporte ao Tk:

```bash
brew install python-tk
```

### Linux

Em distribuições Linux, o Tkinter pode precisar ser instalado separadamente:

#### Ubuntu/Debian:

```bash
sudo apt-get install python3-tk
```

#### CentOS/RHEL/Fedora:

```bash
sudo yum install tkinter
# ou para versões mais recentes:
sudo dnf install python3-tkinter
```

#### Arch Linux:

```bash
sudo pacman -S tk
```

**Importante:** Nunca instale o Tkinter usando `pip install tkinter`, pois isso pode causar problemas. Use sempre os gerenciadores de pacotes do sistema operacional.

## Usage

1. Run the application
2. Select your EPUB file using the file browser
3. Choose output location for the PDF file
4. Click convert to start the conversion process

### Command Line Usage

You can also use the converter from the command line:

```bash
# Basic conversion
python -m src.epubtopdf book.epub --cli

# Specify output file
python -m src.epubtopdf book.epub -o output.pdf --cli

# Use tolerant mode for problematic EPUB files
python -m src.epubtopdf book.epub --cli --tolerant
```

## Troubleshooting

### Tolerant Mode

If you encounter conversion errors, try using the `--tolerant` flag. This mode is designed to handle common issues with malformed EPUB files.

**What the tolerant flag does:**
- Continues conversion even if some paragraphs or images cannot be parsed
- Logs warnings for problematic content instead of stopping with an error
- Skips malformed HTML elements that would otherwise cause conversion failure
- Attempts alternative text extraction methods for problematic paragraphs

**When to use tolerant mode:**
- EPUBs with malformed `<img>` tags inside paragraphs
- Files containing typographic quotes in HTML attributes (e.g., `<img src="image.png"/>` instead of `<img src="image.png"/>`)
- EPUBs with non-self-closed image tags or mixed content in paragraphs
- Complex HTML structures that ReportLab's paragraph parser cannot handle

**Common error messages that indicate you should try tolerant mode:**
- `"paraparser: syntax error: No content allowed in img tag"`
- `"Conversion failed: [HTML parsing error]"`
- Errors related to malformed HTML or XML content

**Example usage:**
```bash
python -m src.epubtopdf problematic_book.epub --cli --tolerant
```

**Note:** Tolerant mode may skip some problematic elements, so some images or special formatting may not appear in the resulting PDF. However, the main text content should be preserved.

### Other Common Issues

**Tkinter not available:** See the "Instalação do Tk" section above for platform-specific installation instructions.

**Permission errors:** Make sure you have write permissions to the output directory.

**Large files:** Very large EPUB files may take longer to convert. Be patient and monitor the progress output.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
