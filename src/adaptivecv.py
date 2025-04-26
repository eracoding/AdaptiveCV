'''
---------------------------------
File: adaptivecv.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
Description: ...
---------------------------------
'''
import os
import json
import validators
import logging
import functools

from typing import Dict, Tuple, Optional, Union, Any
from pathlib import Path

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.models.sections import Resume
from src.utils import utils
from src.utils.latex_ops import latex_to_pdf
from src.utils.llm_models import ChatGPT
from src.utils.data_processing import read_data_from_url, extract_text
from src.utils.metrics import jaccard_similarity, overlap_coefficient, cosine_similarity, vector_embedding_similarity
from src.prompts.resume_prompt import CV_GENERATOR, RESUME_DETAILS_EXTRACTOR, CV_EXPERT, JOB_DETAILS_EXTRACTOR
from src.models.jobs import JobData
from src.envs import DEFAULT_LLM_MODEL, DEFAULT_LLM_PROVIDER, LLM_MAPPING, section_mapping


# Set up logging
logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


# Set module directory paths
MODULE_DIR = Path(__file__).parent
DEMO_DATA_PATH = MODULE_DIR / "demo" / "user_profile.json"


class AdaptiveCV:
    """
    AdaptiveCV for job applications.

    This model extracts job details from URLs, extracts user data from resumes,
    and generates tailored resumes and cover letters based on job descriptions.

    Args:
        api_key (str, optional): The API key for the LLM provider. Defaults to environment variable.
        downloads_dir (str, optional): The directory to save generated files. Defaults to system downloads folder.
        provider (str, optional): The LLM provider to use. Defaults to DEFAULT_LLM_PROVIDER.
        model (str, optional): The LLM model to use. Defaults to DEFAULT_LLM_MODEL.
        system_prompt (str, optional): Custom system prompt. Defaults to RESUME_WRITER_PERSONA.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        downloads_dir: Optional[str] = None,
        system_prompt: str = CV_EXPERT
    ):
        self.system_prompt = system_prompt
        self.provider = DEFAULT_LLM_PROVIDER if not provider or not provider.strip() else provider
        self.model = DEFAULT_LLM_MODEL if not model or not model.strip() else model
        self.downloads_dir = utils.get_default_download_folder() if not downloads_dir or not downloads_dir.strip() else downloads_dir

        self.api_key = self._get_api_key(api_key)

        logger.info(f"Initializing {self.provider} model: {self.model}")
        self.llm = self._get_llm_instance()


    def _get_api_key(self, api_key: Optional[str]) -> Optional[str]:
        """Get API Key"""
        if not api_key or api_key.strip() == "os":
            api_env = LLM_MAPPING[self.provider].get("api_env")
            if api_env and api_env.strip():
                env_key = os.environ.get(api_env)
                if not env_key:
                    logger.warning(f"API key environment variable {api_env} not found")
                return env_key
            return None
        return api_key
    

    def _get_llm_instance(self):
        """Create and return the appropriate LLM instance based on provider"""
        providers = {
            "GPT": lambda: ChatGPT(api_key=self.api_key, model=self.model, system_prompt=self.system_prompt), # for now only chatgpt
        }

        if self.provider not in providers:
            raise ValueError(f"Invalid LLM Provider: {self.provider}. Supported providers: {', '.join(providers.keys())}")
        
        return providers[self.provider]()
    

    def resume_to_json(self, pdf_path: str) -> Dict:
        """
        Converts a resume in PDF format to JSON format.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            dict: The resume data in JSON format.
        """
        logger.info(f"Extracting text from PDF: {pdf_path}")
        resume_text = extract_text(pdf_path)

        if not resume_text:
            logger.error("Failed to extract from PDF")
            raise ValueError("Could not extract text from the provided PDF")
        
        logger.info("Parsing resume text to JSON format")
        json_parser = JsonOutputParser(pydantic_object=Resume)

        prompt = PromptTemplate(
            template=RESUME_DETAILS_EXTRACTOR,
            input_variables=["resume_text"],
            partial_variables={"format_instructions": json_parser.get_format_instructions()}
        ).format(resume_text=resume_text)

        resume_json = self.llm.get_response(prompt=prompt, need_json_output=True)
        logger.info("Resume Successfully parsed to JSON")

        return resume_json

    @utils.timer_decoder
    def user_data_extraction(self, user_data_path: Optional[str] = None, is_st: bool = False) -> Dict:
        """
        Extracts user data from the given file path or URL.

        Args:
            user_data_path (str, optional): Path to user data file or URL. Defaults to demo data.
            is_st (bool, optional): Whether Streamlit is being used. Defaults to False.

        Returns:
            dict: The extracted user data in JSON format.

        Raises:
            ValueError: If the file format is invalid or file cannot be processed.
        """
        logger.info("Starting user data extraction")

        # Using demo if not data provided
        if not user_data_path:
            user_data_path = str(DEMO_DATA_PATH)
            logger.info("No user data path provided, using demo data: {user_data_path}")
        
        # Handle URL
        if validators.url(user_data_path):
            logger.info(f"Extracting user data from URL: {user_data_path}")
            user_data = read_data_from_url([user_data_path])
            if not user_data:
                raise ValueError(f"Failed to extract data from URL: {user_data_path}")
            return user_data

        # Handle file
        path = Path(user_data_path)
        if not path.exists():
            raise FileNotFoundError(f"User data file not found: {user_data_path}")
        
        extension = path.suffix.lower()

        if extension == '.pdf':
            logger.info(f"Processing PDF resume: {user_data_path}")
            return self.resume_to_json(user_data_path)
        elif extension == '.json':
            logger.info(f"Loading JSON user data: {user_data_path}")
            return utils.read_json(user_data_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}. Please provide a PDF, JSON file, or URL.")
        
    
    @utils.timer_decoder
    def job_details_extraction(self, url: Optional[str] = None, job_site_content: Optional[str] = None, is_st: bool = False) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Extracts job details from a URL or job description content.

        Args:
            url (str, optional): The URL of the job posting.
            job_site_content (str, optional): The content of the job posting.
            is_st (bool, optional): Whether Streamlit is being used. Defaults to False.

        Returns:
            Tuple[Optional[Dict], Optional[str]]: Job details dictionary and path to saved JSON file.

        Raises:
            ValueError: If neither URL nor job content is provided.
        """
        logger.info("Starting job details extraction")

        if not url and not job_site_content:
            logger.error("No job url or content provided")
            raise ValueError("Either a job URL or job description content must be provided")
        
        try:
            if url and not job_site_content:
                logger.info(f"Fetching job content from URL: {url}")
                job_site_content = read_data_from_url(url)
                if not job_site_content:
                    logger.error(f"Failed to fetch content from URL: {url}")
                    # if is_st:
                    #     import streamlit as st
                    #     st.error("Failed to fetch job description from URL. Please try pasting the job description text instead.")
                    raise ValueError(f"Could not fetch job description from URL: {url}")
            
            # Parse job details
            logger.info("Parsing job details from content")
            json_parser = JsonOutputParser(pydantic_object=JobData)

            prompt = PromptTemplate(
                template=JOB_DETAILS_EXTRACTOR,
                input_variables=["job_description"],
                partial_variables={"format_instructions": json_parser.get_format_instructions()}
            ).format(job_description=job_site_content)

            job_details = self.llm.get_response(prompt=prompt, need_json_output=True)
            if not job_details:
                logger.error("LLM failed to parse job details")
                raise ValueError("Failed to parse job details from the provided content")
            
            if url:
                job_details["url"] = url
            
            # Save job details
            jd_path = utils.job_doc_name(job_details, self.downloads_dir, "jd")
            utils.write_json(jd_path, job_details)
            logger.info(f"Job details saved to: {jd_path}")

            # Remove URL from returned dictionary if added earlier
            if url:
                job_details.pop('url', None)

            return job_details, jd_path

        except Exception as e:
            logger.exception(f"Error extracting job details: {str(e)}")
            # if is_st:
            #     import streamlit as st
            #     st.error(f"Error in job details parsing: {str(e)}")
            return None, None
        
    @utils.timer_decoder
    def cover_letter_generator(self, job_details: Dict, user_data: Dict, need_pdf: bool = True, is_st: bool = False) -> Tuple[Optional[str], Optional[str]]:
        """
        Generates a cover letter based on job details and user data.

        Args:
            job_details (Dict): Job description details.
            user_data (Dict): User's resume or work information.
            need_pdf (bool, optional): Whether to generate a PDF. Defaults to True.
            is_st (bool, optional): Whether Streamlit is being used. Defaults to False.

        Returns:
            Tuple[Optional[str], Optional[str]]: Cover letter text and path to PDF file.
        """

        logger.info("Starting cover letter generation")

        try:
            # print(type(job_details), job_details)
            # print(type(user_data), user_data)
            prompt = PromptTemplate(
                template=CV_GENERATOR,
                input_types={
                    "my_work_information": dict,
                    "job_description": dict,
                },
            )
            formatted_prompt = prompt.format(
                job_description=job_details,
                my_work_information=user_data,
            )
            # prompt = PromptTemplate(
            #     template=CV_GENERATOR,
            #     input_types=["my_work_information", "job_description"],
            # ).format(job_description=job_details, my_work_information=user_data)

            logger.info("Generating cover letter with LLM")
            cover_letter = self.llm.get_response(prompt=formatted_prompt, expecting_longer_output=True)
            if not cover_letter:
                logger.error("Failed to generate Cover Letter")
                return None, None
            
            cover_letter = utils.clean_text(cover_letter)
            
            # Save cover letter as text
            cv_path = utils.job_doc_name(job_details, self.downloads_dir, "cv")
            utils.write_file(cv_path, cover_letter)
            logger.info(f"Cover Letter text saved to: {cv_path}")

            # Generate PDF if needed
            pdf_path = None
            if need_pdf:
                pdf_path = cv_path.replace(".txt", ".pdf")
                utils.text_to_pdf(cover_letter, pdf_path)
                logger.info(f"Cover letter PDF generated at: {pdf_path}")

            return cover_letter, pdf_path
        
        except Exception as e:
            logger.exception(f"Error generating cover letter: {str(e)}")
            # if is_st:
            #     import steamlit as st
            #     st.error(f"Error generating cover letter: {str(e)}")
            return None, None
        
    
    @utils.timer_decoder
    def resume_builder(self, job_details: Dict, user_data: Dict, is_st: bool = False) -> Tuple[str, Dict]:
        """
        Builds a tailored resume based on job details and user data.

        Args:
            job_details (Dict): Job description details.
            user_data (Dict): User's resume or work information.
            is_st (bool, optional): Whether Streamlit is being used. Defaults to False.

        Returns:
            Tuple[str, Dict]: Path to generated PDF resume and resume details dictionary.
        """
        logger.info("Starting resume generation")
        resume_details = {}
        resume_path = ""

        try:
            # Create personal information section
            logger.info("Processing personal information section")
            resume_details["personal"] = {
                "full_name": user_data["full_name"],
                "contact_number": user_data["contact_number"],
                "email_address": user_data["email_address"],
                "github": user_data["media_profiles"]["github"],
                "linkedin": user_data["media_profiles"]["linkedin"]
            }

            # if is_st:
            #     import streamlit as st
            #     st.toast("Processing Resume's Personal Info Section...")
            #     st.markdown("**Personal Info Section**")
            #     st.write(resume_details)

            # Process else sections
            sections = ['work_experience', 'projects', 'skill_section', 'education', 'certifications', 'achievements']
            for section in sections:
                section_log = f"Processing {section.upper()} section"
                logger.info(section_log)

                # if is_st:
                #     st.toast(f"Processing Resume's {section.upper()} Section...")
                
                # Set up json parser
                json_parser = JsonOutputParser(pydantic_object=section_mapping[section]["schema"])

                section_data = user_data.get(section, {})
                # section_data_str = utils.escape_curly_braces(json.dumps(section_data, indent=2, ensure_ascii=False))
                # job_description_str = utils.escape_curly_braces(json.dumps(job_details, indent=2, ensure_ascii=False))
                section_data_str = json.dumps(section_data, indent=2, ensure_ascii=False)
                job_description_str = json.dumps(job_details, indent=2, ensure_ascii=False)

                # Creating prompt per section
                prompt = PromptTemplate(
                    template=section_mapping[section]["prompt"],
                    input_variables=["section_data", "job_description"],
                    partial_variables={"format_instructions": json_parser.get_format_instructions()}
                ).format(
                    section_data=section_data_str,
                    job_description=job_description_str
                )

                # Get LLM Response
                response = self.llm.get_response(
                    prompt=prompt,
                    expecting_longer_output=True,
                    need_json_output=True,
                )

                if response and isinstance(response, dict):
                    if section in response and response[section]:
                        if section == "skill_section":
                            skills = []
                            for skill in response['skill_section']:
                                if skill.get('items') and len(skill['items']):
                                    limited_items = skill['items'][:5]
                                    skills.append({
                                        'title': skill['title'],
                                        'items': limited_items
                                    })

                            resume_details[section] = skills
                        else:
                            resume_details[section] = response[section]
                
                # Display in Streamlit if needed
                # if is_st:
                #     st.markdown(f"**{section.upper()} Section**")
                #     st.write(response)
            
            # Keywords
            resume_details['keywords'] = ", ".join(job_details.get('keywords', []))

            # Save resume to JSON
            resume_path = utils.job_doc_name(job_details, self.downloads_dir, "resume")
            utils.write_json(resume_path, resume_details)
            logger.info(f"Resume JSON saved to: {resume_path}")

            # Generate PDF
            pdf_path = resume_path.replace(".json", ".pdf")
            logger.info(f"Generating PDF resume at: {pdf_path}")
            latex_to_pdf(resume_details, pdf_path)
            logger.info(f"Resume PDF generated at: {pdf_path}")

            return pdf_path, resume_details            

        except Exception as e:
            logging.error(f"Error building resume: {e}")
            # if is_st:
            #     import streamlit as st
            #     st.error(f"Error building resume: {str(e)}")
            return resume_path, resume_details
    

    def calculate_metrics(self, resume_details: Dict, user_data: Dict, job_details: Dict) -> Dict[str, Dict[str, float]]:
        """
        Calculate similarity metrics between resume, user data, and job details.
        
        Args:
            resume_details (Dict): Generated resume details
            user_data (Dict): Original user data
            job_details (Dict): Job description details
            
        Returns:
            Dict: Dictionary of metrics with scores
        """
        logger.info("Calculating similarity metrics")
        metrics = {}

        for metric_name in ['jaccard_similarity', 'overlap_coefficient', 'cosine_similarity']:
            # jaccard_similarity, overlap_coefficient, cosine_similarity, vector_embedding_similarity
            logger.info(f"Calculating {metric_name}")
            metric_func = globals()[metric_name]

            resume_str = json.dumps(resume_details)
            user_str = json.dumps(user_data)
            job_str = json.dumps(job_details)


            user_personalization = metric_func(resume_str, user_str)
            job_alignment = metric_func(resume_str, job_str)
            job_match = metric_func(user_str, job_str)

            metrics[metric_name] = {
                "user_personalization": user_personalization,
                "job_alignment": job_alignment,
                "job_match": job_match
            }

            logger.info(f"{metric_name} - User Personalization: {user_personalization:.4f}, "
                        f"Job Alignment: {job_alignment:.4f}, Job Match: {job_match:.4f}")
                        
        return metrics


    def resume_cv_pipeline(self, job_url: str, user_data_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the complete Auto Apply Pipeline to generate a resume and cover letter.

        Args:
            job_url (str): The URL of the job to apply for.
            user_data_path (str, optional): Path to the user profile data file.

        Returns:
            Dict: Results including file paths and metrics.
        """
        logger.info("Starting AdaptiveCV Pipeline")
        result = {
            "success": False,
            "files": {},
            "metrics": {}
        }

        # try:
        if not job_url or not job_url.strip():
            logger.error("Job URL is required")
            raise ValueError("Job URL is required")
        
        # Use default user data path if not provided
        if not user_data_path:
            user_data_path = str(DEMO_DATA_PATH)
            logger.info(f"Using default user data path: {user_data_path}")

        # Extracting user data
        logger.info("Extracting user data")
        user_data = self.user_data_extraction(user_data_path)
        if not user_data:
            raise ValueError("Failed to extract user data")
        
        # Extract job details
        logger.info(f"Extracting job details from URL: {job_url}")
        job_details, jd_path = self.job_details_extraction(url=job_url)
        if not job_details:
            raise ValueError("Failed to extract job details")
        
        result["files"]["job_details"] = jd_path

        # Build resume
        logger.info("Building tailored resume")
        resume_path, resume_details = self.resume_builder(job_details, user_data)
        result["files"]["resume"] = resume_path

        # Generate cover letter
        logger.info("Generating cover letter")
        cv_text, cv_path = self.cover_letter_generator(job_details, user_data)
        result["files"]["cover_letter"] = cv_path

        # Calculate metrics
        metrics = self.calculate_metrics(resume_details, user_data, job_details)
        result["metrics"] = metrics

        result["success"] = True
        logger.info("Auto Resume and CV Pipeline completed successfully")
        
        return result
            
        # except Exception as e:
        #     logger.error(f"Error in resume CV Pipeline: {str(e)}")
        #     result["error"] = str(e)
        #     return result
