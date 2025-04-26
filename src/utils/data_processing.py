'''
---------------------------------
File: data_processing.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
---------------------------------
'''
import re
import requests
import logging
import time
import functools

from typing import List, Dict, Optional, Union
from concurrent.futures import ThreadPoolExecutor

import PyPDF2
from bs4 import BeautifulSoup
from langchain_community.document_loaders import (
    PlaywrightURLLoader, 
    UnstructuredURLLoader, 
    WebBaseLoader
)

from src.utils.utils import (
    timer_decoder, error_handler,
    TextCleaner
)


# # Configuring logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

logger = logging.getLogger(__name__)

# Defining selectors for different websites
SELECTORS = {
    "basic": ["header", "footer", "nav", ".ad", ".advertisement", ".cookie-notice"],
    "linkedin": [
        "#main-content > section.right-rail",
        ".job-alert-redirect-section",
        ".similar-jobs",
        ".share-box"
    ],
    "indeed": [
        "#mosaic-modalLightbox",
        "#jobsearch-ViewjobPaneWrapper",
        "#jobsearch-ViewJobButtons"
    ]
}


class WebContentExtractor:
    """Class for extracting content from web pages"""

    @staticmethod
    def _get_selectors_for_url(url: str) -> List[str]:
        """Determine which selectors to use"""
        selectors = SELECTORS["basic"].copy()

        # Add site-specific selectors
        if "linkedin.com" in url:
            selectors.extend(SELECTORS["linkedin"])
        elif "indeed.com" in url:
            selectors.extend(SELECTORS["indeed"])
            
        return selectors
    
    @staticmethod
    @error_handler
    @timer_decoder
    def extract_from_url(url: str) -> Optional[str]:
        """Extract content from url"""
        if not url:
            logger.warning("No URL provided")
            return None
        
        selectors = WebContentExtractor._get_selectors_for_url(url)

        # Try different loaders with error handling
        loaders = [
            PlaywrightURLLoader(urls=[url], remove_selectors=selectors),
            UnstructuredURLLoader(urls=[url], ssl_verify=False, remove_selectors=selectors),
            WebBaseLoader(url)
        ]

        for loader in loaders:
            try:
                pages = loader.load()
                if pages:
                    content = ""
                    for page in pages:
                        if page.page_content.strip():
                            text_list = page.page_content.split('\n')
                            cleaned_texts = TextCleaner.clean_text_list(text_list)
                            content += TextCleaner.join_text_list(cleaned_texts)
                    if content:
                        return content
            except Exception as e:
                logger.debug(f"Loader {loader.__class__.__name__} failed: {str(e)}")
                continue

        # Fallback to simple BS4
        return WebContentExtractor.extract_with_bs4(url)
    
    @staticmethod
    @error_handler
    def extract_with_bs4(url: str) -> Optional[str]:
        """Extract content using BeautifulSoup as a fallback method"""
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status() # Raise exception for bad responses

            soup = BeautifulSoup(res.content, "html.parser")

            # Remove elements
            for selector in ['script', 'style', 'header', 'footer', 'nav']:
                for element in soup.select(selector):
                    element.decompose()

            # Body content
            body = soup.body or soup

            # Extract text content
            text_content = []
            for string in body.stripped_strings:
                if string.strip():
                    text_content.append(string.strip())

            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"BS4 extraction failed: {str(e)}")
            return None
        

class PDFExtractor:
    """Class for extracting content from PDF files"""

    @staticmethod
    @error_handler
    @timer_decoder
    def extract_text(pdf_path: str) -> Optional[str]:
        """Extract text from a PDF file"""
        if not pdf_path:
            logger.warning("No PDF Path provided")
            return None
    
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                # For large pdfs, using parallel processing
                if num_pages > 10:
                    return PDFExtractor._extract_parallel(pdf_reader, num_pages)
                else:
                    return PDFExtractor._extract_sequential(pdf_reader, num_pages)
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return None
        
    @staticmethod
    def _extract_page(pdf_reader, page_num: int) -> str:
        """Extract text form a single page"""
        page = pdf_reader.pages[page_num]
       
        text = page.extract_text().split("\n")
       
        cleaned_text = TextCleaner.clean_text_list(text)
       
        return TextCleaner.join_text_list(cleaned_text)
    
    @staticmethod
    def _extract_sequential(pdf_reader, num_pages: int) -> str:
        """Extract text from PDF page sequentially"""
        all_text = []
    
        for page_num in range(num_pages):
            all_text.append(PDFExtractor._extract_page(pdf_reader, page_num))
    
        return "\n".join(all_text)
    
    @staticmethod
    def _extract_parallel(pdf_reader, num_pages: int) -> str:
        """Extract text from PDF page in parallel"""
        with ThreadPoolExecutor(max_workers=min(num_pages, 8)) as executor:
            extract_fn = functools.partial(PDFExtractor._extract_page, pdf_reader)
            results = list(executor.map(extract_fn, range(num_pages)))
        return "\n".join(results)
    

# Public API functions for backward compatibility
@error_handler
def read_data_from_url(url: str) -> Optional[str]:
    """Extract text content from url"""
    return WebContentExtractor.extract_from_url(url)

@error_handler
def extract_text(pdf_path: str) -> Optional[str]:
    """Extract text from a PDF"""
    return PDFExtractor.extract_text(pdf_path)

@error_handler
def get_url_content(url: str) -> Optional[str]:
    """Legacy function for extracting URL with BS4"""
    return WebContentExtractor.extract_with_bs4(url)


if __name__ == "__main__":
    # Example usage
    url = "https://example.com"
    content = read_data_from_url(url)
    if content:
        print(f"Successfully extracted {len(content)} characters from {url}")
    else:
        print(f"Failed to extract content from {url}")
