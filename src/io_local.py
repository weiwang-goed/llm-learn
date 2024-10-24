from pathlib import Path
import pdfplumber
import docx
import openpyxl
import pandas as pd

def read_pdf(file_path):
    """Reads content from a PDF file"""
    content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content += page.extract_text()
    return content

def read_docx(file_path):
    """Reads content from a DOCX file"""
    doc = docx.Document(file_path)
    content = "\n".join([para.text for para in doc.paragraphs])
    return content

def read_xlsx(file_path):
    """Reads content from an XLSX file"""
    # Using pandas to read all sheets and converting to text
    xls = pd.ExcelFile(file_path)
    content = ""
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        content += df.to_string(index=False, header=False)  # Convert DataFrame to text
    return content

def read_txt(file_path):
    """Reads content from a TXT file"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

def read_file(file_path):
    """Reads content based on file extension"""
    try:
        if file_path.endswith('.pdf'):
            return read_pdf(file_path)
        elif file_path.endswith('.docx'):
            return read_docx(file_path)
        elif file_path.endswith('.xlsx'):
            return read_xlsx(file_path)
        elif file_path.endswith('.txt'):
            return read_txt(file_path)
    except:
        return "Unsupported format or read fail"


def _get_file_meta(path:Path)->dict:
    return {
        'path': str(path), 
        'type': str(path).split('.')[-1],
        'size': path.stat().st_size,
        'date': path.stat().st_mtime
    }

def list_dir_metas(path, filter_types:list = ['pdf', 'xlsx', 'txt', 'docx']):
    folder = Path(path)
    files = [f for f in folder.rglob('*') if f.is_file()]
    files = list(map(_get_file_meta, files)) # info
    files = [f for f in files if f['type'] in filter_types]
    return pd.DataFrame(files)
