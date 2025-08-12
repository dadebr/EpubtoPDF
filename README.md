# EpubtoPDF
A Python application that provides a graphical user interface (GUI) for converting EPUB files to PDF format.

## Features
- Simple and intuitive GUI interface
- Converts EPUB e-books to PDF format
- Easy-to-use file selection and conversion process

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

## License
This project is licensed under the MIT License - see the LICENSE file for details.
