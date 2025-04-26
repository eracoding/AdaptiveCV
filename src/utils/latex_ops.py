'''
---------------------------------
File: latex_ops.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
---------------------------------
'''

import os
import jinja2
import logging
import subprocess
import shutil

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import traceback

import streamlit as st

from src.utils.utils import (
    write_file,
    error_handler,
    timer_decoder
)


# Configure logging
logger = logging.getLogger(__name__)


class LatexProcessor:
    """Latex Processing functions"""

    @staticmethod
    def escape_for_latex(data: Any) -> Any:
        """
        Escapes special LaTeX characters in strings, recursively processing dictionaries and lists
        
        Args:
            data: Input data (dict, list, str, or other type)
            
        Returns:
            Escaped data with LaTeX special characters properly handled
        """

        if isinstance(data, dict):
            new_data = {}
            for key in data.keys():
                new_data[key] = LatexProcessor.escape_for_latex(data[key])
            return new_data
        elif isinstance(data, list):
            return [LatexProcessor.escape_for_latex(item) for item in data]
        elif isinstance(data, str):
            # Adapted from https://stackoverflow.com/q/16259923
            latex_special_chars = {
                "&": r"\&",
                "%": r"\%",
                "$": r"\$",
                "#": r"\#",
                "_": r"\_",
                "{": r"\{",
                "}": r"\}",
                "~": r"\textasciitilde{}",
                "^": r"\^{}",
                "\\": r"\textbackslash{}",
                "\n": "\\newline%\n",
                "-": r"{-}",
                "\xA0": "~",  # Non-breaking space
                "[": r"{[}",
                "]": r"{]}",
            }
            return "".join([latex_special_chars.get(c, c) for c in data])

        return data

    @staticmethod
    @error_handler
    def get_jinja_env(templates_path: str) -> jinja2.Environment:
        """
        Creates and configures a Jinja2 environment for LaTeX templates
        
        Args:
            templates_path: Path to the template directory
            
        Returns:
            Configured Jinja2 Environment
        """
        return jinja2.Environment(
            block_start_string="\BLOCK{",
            block_end_string="}",
            variable_start_string="\VAR{",
            variable_end_string="}",
            comment_start_string="\#{",
            comment_end_string="}",
            line_statement_prefix="%-",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(templates_path),
        )
    

    @staticmethod
    @error_handler
    def use_template(jinja_env: jinja2.Environment, json_resume: Dict) -> Optional[str]:
        """
        Renders the resume template with the provided JSON data
        """
        try:
            # Print available templates for debugging
            templates = jinja_env.list_templates()
            print(f"Available templates: {templates}")
            
            if "resume.tex.jinja" not in templates:
                print("Error: resume.tex.jinja template not found!")
                return None
                
            resume_template = jinja_env.get_template("resume.tex.jinja")
            
            # Print resume data keys for debugging
            print(f"Resume data keys: {json_resume.keys()}")
            if 'personal' in json_resume:
                print(f"Personal data keys: {json_resume['personal'].keys()}")
            
            # Render the template
            resume = resume_template.render(**json_resume)
            
            # Write intermediate file for debugging
            debug_file = "debug_template_output.tex"
            with open(debug_file, "w") as f:
                f.write(resume)
            print(f"Wrote debug output to {debug_file}")
            
            return resume
        except Exception as e:
            print(f"Error rendering Latex template: {str(e)}")
            traceback.print_exc()
            return None

    @staticmethod
    @error_handler
    def save_latex_as_pdf(tex_file_path: str, dst_path: str) -> Optional[str]:
        """Convert Latex to PDF using pdflatex"""
        try:
            prev_loc = os.getcwd()
            tex_dir = os.path.dirname(tex_file_path)
            tex_filename = os.path.basename(tex_file_path)
            
            # Change to the directory containing the .tex file
            os.chdir(tex_dir)
            
            # Run pdflatex twice to resolve references
            for i in range(2):
                print(f"Running pdflatex iteration {i+1}...")
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", tex_filename],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Print output for debugging
                print(f"pdflatex stdout: {result.stdout[:500]}...")  # Print first 500 chars
                print(f"pdflatex stderr: {result.stderr}")
                
                if result.returncode != 0:
                    print(f"pdflatex returned non-zero exit code: {result.returncode}")
            
            # Change back to original directory
            os.chdir(prev_loc)
            
            # Paths for generated files
            resulted_pdf_path = tex_file_path.replace(".tex", ".pdf")
            dst_tex_path = dst_path.replace(".pdf", ".tex")
            
            # Check if PDF was actually created
            if not os.path.exists(resulted_pdf_path):
                print(f"Error: PDF file was not created at {resulted_pdf_path}")
                return None
                
            # Move the files
            shutil.move(resulted_pdf_path, dst_path)
            shutil.move(tex_file_path, dst_tex_path)
            
            # Clean up auxiliary files
            filename_without_ext = os.path.splitext(tex_filename)[0]
            for ext in ['.aux', '.log', '.out', '.toc']:
                aux_file = os.path.join(tex_dir, f"{filename_without_ext}{ext}")
                if os.path.exists(aux_file):
                    os.remove(aux_file)
                    
            return dst_path
            
        except Exception as e:
            print(f"Exception in save_latex_as_pdf: {str(e)}")
            traceback.print_exc()
            return None
        
    @staticmethod
    def validate_resume_data(json_resume: Dict) -> bool:
        """Validate that all required fields are present in the resume data"""
        required_fields = ['personal']
        
        for field in required_fields:
            if field not in json_resume:
                print(f"Missing required field '{field}' in resume data")
                return False
                
        # Check personal section
        if 'personal' in json_resume:
            personal_required = ['full_name']
            for field in personal_required:
                if field not in json_resume['personal']:
                    print(f"Missing required field 'personal.{field}' in resume data")
                    return False
                    
        return True
    

@timer_decoder
@error_handler
def latex_to_pdf(json_resume: Dict, dst_path: str) -> Optional[str]:
    """
    Converts JSON resume data to a PDF document via LaTeX
    
    Args:
        json_resume: Resume data in dictionary format
        dst_path: Destination path for the PDF file
        
    Returns:
        LaTeX content as string if successful, None otherwise
    """

    # try:
    # Template dir
    module_dir = os.path.dirname(__file__)
    templates_path = os.path.join(os.path.dirname(module_dir), 'templates')

    # Make sure templates directory exists
    # print(f"Templates path: {templates_path}")
    if not os.path.exists(templates_path):
        print(f"Error: Templates directory does not exist: {templates_path}")
        return None

    # Check if resume.tex.jinja exists
    template_file = os.path.join(templates_path, "resume.tex.jinja")
    if not os.path.exists(template_file):
        print(f"Error: Template file does not exist: {template_file}")
        return None

    # Create Jinja environment
    # print("Setting up Jinja environment...")
    latex_jinja_env = LatexProcessor.get_jinja_env(templates_path)
    if not latex_jinja_env:
        print("Failed to create Jinja environment")
        return None

    # Print JSON resume structure before escaping (for debugging)
    # print("Original JSON structure:")
    # print(f"Keys: {json_resume.keys()}")

    # Escape Latex special characters
    # print("Escaping LaTeX special characters...")
    escaped_json_resume = LatexProcessor.escape_for_latex(json_resume)

    # Validate the data
    if not LatexProcessor.validate_resume_data(escaped_json_resume):
        print("Invalid resume data")
        return None

    # Render Latex Template
    # print("Rendering LaTeX template...")
    resume_latex = LatexProcessor.use_template(latex_jinja_env, escaped_json_resume)
    if not resume_latex:
        print("Failed to render LaTeX template")
        return None

    # Save Latex
    tex_temp_path = os.path.join(templates_path, os.path.basename(dst_path).replace(".pdf", ".tex"))
    # print(f"Writing LaTeX to {tex_temp_path}")

    # Write file
    try:
        with open(tex_temp_path, 'w') as f:
            f.write(resume_latex)
    except Exception as e:
        print(f"Error writing LaTeX file: {str(e)}")
        return None

    # Convert to PDF
    # print(f"Converting LaTeX to PDF: {tex_temp_path} -> {dst_path}")
    pdf_path = LatexProcessor.save_latex_as_pdf(tex_temp_path, dst_path)

    if pdf_path:
        print(f"Successfully created PDF: {pdf_path}")
        return pdf_path
    else:
        print("Failed to create PDF")
        return None

# For backward compatibility
escape_for_latex = LatexProcessor.escape_for_latex
use_template = LatexProcessor.use_template
