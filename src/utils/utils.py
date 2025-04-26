'''
---------------------------------
File: utils.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
---------------------------------
'''
import os
import re
import time
import json
import base64
import logging
import subprocess
import functools
import unicodedata
import platform
import shutil

import streamlit as st
import streamlit.components.v1 as components

from fpdf import FPDF
from markdown_pdf import MarkdownPdf, Section
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Callable


# Constants
OS_SYSTEM = platform.system().lower()
DEFAULT_ENCODING = 'utf-8'


# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    # Normalize Unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Remove non-printable characters
    # text = ''.join(c for c in text if c.isprintable())

    # Replace smart quotes and dashes with ASCII equivalents
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('‘', "'").replace('’', "'")
    text = text.replace('–', '-').replace('—', '-')

    # # Remove extra invisible characters (e.g., \u200b, \ufeff)
    # text = re.sub(r'[\u200b-\u200f\u202a-\u202e\ufeff]', '', text)

    return text.strip()

def escape_curly_braces(text):
    return text.replace("{", "{{").replace("}", "}}")

# Decorators
def timer_decoder(func: Callable) -> Callable:
    """Measure execution time of functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f"Function {func.__name__} took {end_time - start_time:.2f} seconds to run")
        return result
    return wrapper

def error_handler(func: Callable) -> Callable:
    """Handle exceptions in functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper


class TextCleaner:
    """Utility class for text cleaning operations"""

    @staticmethod
    def remove_unicode(text: str) -> str:
        """Remove non-ASCII characters"""
        return re.sub(r'[^\x00-\x7F]+', '', text)
    
    @staticmethod
    def clean_string(text: str) -> str:
        """Clean a string"""
        text = text.title().replace(" ", "").strip()
        return re.sub(r"[^a-zA-Z0-9]+", "", text)
    
    @staticmethod
    def clean_text_list(text_list: List[str]) -> List[str]:
        """Clean strings"""
        cleaned = [TextCleaner.remove_unicode(text) for text in text_list]

        return [text.strip() for text in cleaned if text.strip()]
    
    @staticmethod
    def join_text_list(text_list: List[str]) -> str:
        """Join into string"""
        return '\n'.join(text_list)
    

class FileHandler:
    """Class for file handling operations"""

    @staticmethod
    def write_file(file_path: str, data: str, mode: str = 'w') -> None:
        """Write data into file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(data)
    
    @staticmethod
    def read_file(file_path: str, mode: str = 'r') -> str:
        """Read data from file"""
        with open(file_path, mode) as file:
            return file.read()

    @staticmethod
    def write_json(file_path: str, data: Any) -> None:
        """Write data into JSON"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def read_json(file_path: str) -> Dict:
        """Read data from JSON"""
        with open(file_path, 'r') as file:
            return json.load(file)
    

class PathManager:
    """Class for managing file paths and directories"""

    @staticmethod
    def job_doc_name(job_details: Dict, output_dir: str = "output", type: str = "") -> str:
        """Generate filepath for job-related docs"""
        company_name = TextCleaner.clean_string(job_details["company_name"])
        job_title = TextCleaner.clean_string(job_details["title"])[:15]
        doc_name = "_".join([company_name, job_title])
        doc_dir = os.path.join(output_dir, company_name)
        os.makedirs(doc_dir, exist_ok=True)

        if type == 'jd':
            return os.path.join(doc_dir, f"{doc_name}_JD.json")
        elif type == 'resume':
            return os.path.join(doc_dir, f"{doc_name}_resume.json")
        elif type == 'cv':
            return os.path.join(doc_dir, f"{doc_name}_cv.txt")
        else:
            return os.path.join(doc_dir, f"{doc_name}_")
        
    
    @staticmethod
    def get_default_download_folder() -> str:
        """Default download folder"""
        root = "/mnt/c/Users/eraco/"
        download_folder_path = os.path.join(root, "Downloads", "AdaptiveCV_Resume_CV")
        os.makedirs(download_folder_path, exist_ok=True)
        return download_folder_path


    @staticmethod
    def save_log(content: Any, file_name: str) -> None:
        """Save content to log with timestamp"""
        timestamp = int(datetime.timestamp(datetime.now()))
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        file_path = f"{log_dir}/{file_name}_{timestamp}.txt"
        FileHandler.write_file(file_path, str(content))



class FileOpener:
    """Class for opening files with the appropriate system"""

    @staticmethod
    def open_file(file: str) -> None:
        """Open a file using system's default application"""
        try:
            if OS_SYSTEM == 'darwin': # macOS
                subprocess.Popen(["open", file])
            elif OS_SYSTEM == "windows":
                os.startfile(file)
            else: # linux
                subprocess.Popen(["xdg-open", file])
        except Exception as e:
            logger.error(f"Error opening file: {e}")



class DocumentConverter:
    """Class converting docs"""

    @staticmethod
    def text_to_pdf(text: str, file_path: str) -> None:
        """Convert to pdf"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            pdf = MarkdownPdf(toc_level=2)
            encoded_text = text.encode(DEFAULT_ENCODING).decode('latin-1')
            pdf.add_section(Section(encoded_text), user_css="body {font-size: 12pt; font-family: Calibri; text-align: justify;}")
            pdf.meta['title'] = "Cover Letter"
            pdf.meta['author'] = "Ulugbek Shernazarov"
            pdf.save(file_path)
        except Exception as e:
            logger.error(f"Error converting text to PDF: {e}")

    @staticmethod
    def safe_latex_as_pdf(tex_file_path: str, dst_path: str) -> Optional[str]:
        """Convert Latex to PDF using pdflatex"""

        try:
            prev_loc = os.getcwd()
            os.chdir(os.path.dirname(tex_file_path))
            try:
                result = subprocess.run(
                    ["pdflatex", os.path.basename(tex_file_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            except Exception as e:
                print("Pdflatex failed to convert tex file to pdf.")
                print(e)
                os.chdir(prev_loc)
                return None

            os.chdir(prev_loc)
            resulted_pdf_path = tex_file_path.replace(".tex", ".pdf")
            dst_tex_path = dst_path.replace(".pdf", ".tex")

            # Use shutil.move instead of os.rename to handle cross-device moves
            shutil.move(resulted_pdf_path, dst_path)
            shutil.move(tex_file_path, dst_tex_path)

            if result.returncode != 0:
                print("Exit-code not 0, check result!")
            try:
                pass
                # open_file(dst_path)
            except Exception as e:
                print("Unable to open the PDF file.")

            filename_without_ext = os.path.basename(tex_file_path).split(".")[0]
            unnessary_files = [
                file
                for file in os.listdir(os.path.dirname(os.path.realpath(tex_file_path)))
                if file.startswith(filename_without_ext)
            ]

            for file in unnessary_files:
                file_path = os.path.join(os.path.dirname(tex_file_path), file)
                if os.path.exists(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(e)
            return None


class StreamlitHelper:
    """Helper class for Streamlit functions"""

    @staticmethod
    def download_pdf(pdf_path: str) -> None:
        """Create automatic download link for pdf file"""

        try:
            bytes_data = FileHandler.read_file(pdf_path, 'rb')
            base64_pdf = base64.b64encode(bytes_data).decode(DEFAULT_ENCODING)

            dl_link = f"""
            <html>
            <head>
            <title>Start Auto Download file</title>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
            $('<a href="data:application/pdf;base64,{base64_pdf}" download="{os.path.basename(pdf_path)}">')[0].click().remove();
            </script>
            </head>
            </html>
            """
            components.html(dl_link, height=0)
        except Exception as e:
            logger.error(f"Error downloading PDF: {e}")


    @staticmethod
    def display_pdf(file: str, type: str = "pdf") -> None:
        """Display PDF file in Streamlit"""
        try:
            if type == 'image':
                # Remove circular imports
                from pdf2image import convert_from_path

                pages = convert_from_path(file)
                for page in pages:
                    st.image(page, use_column_width=True)

            elif type == 'pdf':
                bytes_data = FileHandler.read_file(file, "rb")

                try:
                    base64_pdf = base64.b64encode(bytes_data).decode(DEFAULT_ENCODING)
                except Exception:
                    base64_pdf = base64.b64encode(bytes_data)

                # Iframe Embedding of PDF in HTML
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" type="application/pdf" style="width:100%; height:100vh;"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            
        except Exception as e:
            logger.error(f"Error displaying PDF: {e}")
            st.error(f"Error displaying PDF: {e}")


class JSONParser:
    """Class for parsing JSON from various formats"""

    @staticmethod
    def parse_json_markdown(json_string: str) -> Optional[Dict]:
        """Parse JSON from markdown-formatted string"""
        try:
            # No circular imports
            from langchain_core.output_parsers import JsonOutputParser

            if not json_string:
                return None
            
            # Remove markdown code formatting
            if json_string.startswith("```") and json_string.endswith("```"):
                json_string = json_string[3:-3].strip()
            
            # Remove language specifiers
            if json_string.startswith("typescript") or json_string.startswith("json"):
                json_string = re.sub(r'^(typescript|json)\s*', '', json_string)

            # Remove special markers
            json_string = json_string.replace("JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA", "")
            
            # Parse with JsonOutputParser
            parser = JsonOutputParser()
            parsed = parser.parse(json_string)
            return parsed
        except Exception as e:
            logger.error(f"Error parsing JSON markdown: {e}")
            return None
    

    @staticmethod
    def key_value_chunking(data: Any, prefix: str = "") -> List[str]:
        """Chunk dictionary or list into key-value pairs"""
        chunks = []

        def stop_needed(value):
            return '.' if not isinstance(value, (str, int, float, bool, list)) else ''

        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    chunks.extend(JSONParser.key_value_chunking(
                        value, prefix=f"{prefix}{key}{stop_needed(value)}"
                    ))
        elif isinstance(data, list):
            for index, value in enumerate(data):
                if value is not None:
                    chunks.extend(JSONParser.key_value_chunking(
                        value, prefix=f"{prefix}_{index}{stop_needed(value)}"
                    ))
        else:
            if data is not None:
                chunks.append(f"{prefix}: {data}")
        
        return chunks

def get_prompt(system_prompt_path: str) -> str:
    """
    Reads the content of the file at the given system_prompt_path.
    
    Args:
        system_prompt_path (str): The path to the system prompt file.
    
    Returns:
        str: The content of the file as a string.
    """
    try:
        with open(system_prompt_path, encoding=DEFAULT_ENCODING) as file:
            return file.read().strip() + "\n"
    except Exception as e:
        logger.error(f"Error reading prompt file: {e}")
        return ""


# Legacy function aliases for backward compatibility
write_file = FileHandler.write_file
read_file = FileHandler.read_file
write_json = FileHandler.write_json
read_json = FileHandler.read_json
job_doc_name = PathManager.job_doc_name
clean_string = TextCleaner.clean_string
open_file = FileOpener.open_file
save_log = PathManager.save_log
text_to_pdf = DocumentConverter.text_to_pdf
download_pdf = StreamlitHelper.download_pdf
display_pdf = StreamlitHelper.display_pdf
save_latex_as_pdf = DocumentConverter.safe_latex_as_pdf
get_default_download_folder = PathManager.get_default_download_folder
parse_json_markdown = JSONParser.parse_json_markdown
key_value_chunking = JSONParser.key_value_chunking
