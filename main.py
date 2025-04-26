'''
-----------------------------------------------------------------------
File: test_adaptivecv.py
Description: Testing script for the AdaptiveCV pipeline
-----------------------------------------------------------------------
'''
import os
import argparse
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('adaptivecv_test.log')
    ]
)
logger = logging.getLogger(__name__)

try:
    from src import AdaptiveCV
    logger.info("Successfully imported AdaptiveCV")
except ImportError as e:
    logger.error(f"Failed to import AdaptiveCV: {e}")
    raise

def test_user_data_extraction(model, user_data_path):
    """Test user data extraction functionality."""
    logger.info(f"Testing user data extraction with path: {user_data_path}")
    try:
        user_data = model.user_data_extraction(user_data_path)
        logger.info(f"Successfully extracted user data with {len(user_data)} fields")
        return user_data
    except Exception as e:
        logger.error(f"Failed to extract user data: {e}")
        return None

def test_job_details_extraction(model, job_url):
    """Test job details extraction functionality."""
    logger.info(f"Testing job details extraction with URL: {job_url}")
    try:
        job_details, jd_path = model.job_details_extraction(url=job_url)
        if job_details:
            logger.info(f"Successfully extracted job details with {len(job_details)} fields")
            logger.info(f"Job details saved to: {jd_path}")
        else:
            logger.warning("Job details extraction returned None")
        return job_details, jd_path
    except Exception as e:
        logger.error(f"Failed to extract job details: {e}")
        return None, None

def test_resume_builder(model, job_details, user_data):
    """Test resume builder functionality."""
    logger.info("Testing resume builder")
    try:
        resume_path, resume_details = model.resume_builder(job_details, user_data)
        logger.info(f"Resume built successfully and saved to: {resume_path}")
        return resume_path, resume_details
    except Exception as e:
        logger.error(f"Failed to build resume: {e}")
        return None, None

def test_cover_letter_generator(model, job_details, user_data):
    """Test cover letter generator functionality."""
    logger.info("Testing cover letter generator")
    try:
        cover_letter, cv_path = model.cover_letter_generator(job_details, user_data)
        logger.info(f"Cover letter generated successfully and saved to: {cv_path}")
        return cover_letter, cv_path
    except Exception as e:
        logger.error(f"Failed to generate cover letter: {e}")
        return None, None

def test_full_pipeline(model, job_url, user_data_path):
    """Test the complete resume-CV pipeline."""
    logger.info(f"Testing full pipeline with job URL: {job_url} and user data: {user_data_path}")
    try:
        result = model.resume_cv_pipeline(job_url, user_data_path)
        if result["success"]:
            logger.info("Pipeline completed successfully!")
            logger.info(f"Generated files: {json.dumps(result['files'], indent=2)}")
            logger.info(f"Metrics: {json.dumps(result['metrics'], indent=2)}")
        else:
            logger.error(f"Pipeline failed: {result.get('error', 'Unknown error')}")
        return result
    except Exception as e:
        logger.error(f"Pipeline execution failed with exception: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Test the AdaptiveCV")
    parser.add_argument("--provider", type=str, default="GPT", help="LLM provider (Gemini, GPT, Ollama)")
    parser.add_argument("--model", type=str, default="gpt-4o", help="LLM model name")
    parser.add_argument("--api-key", type=str, default="os", help="API key or 'os' to use environment variable")
    parser.add_argument("--job-url", type=str, required=True, help="URL of the job posting")
    parser.add_argument("--user-data", type=str, help="Path to user data file (PDF or JSON)")
    parser.add_argument("--downloads-dir", type=str, help="Directory to save generated files")
    parser.add_argument("--test-mode", type=str, default="full", 
                        choices=["full", "user-data", "job-details", "resume", "cover-letter"],
                        help="Test mode to run")
    
    args = parser.parse_args()
    
    # Initialize the model
    logger.info(f"Initializing AdaptiveCV with provider: {args.provider}, model: {args.model}")
    try:
        model = AdaptiveCV(
            api_key=args.api_key,
            provider=args.provider,
            model=args.model,
            downloads_dir=args.downloads_dir
        )
        logger.info("AdaptiveCV initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AdaptiveCV: {e}")
        return
    
    # Run the selected test mode
    if args.test_mode == "user-data":
        user_data = test_user_data_extraction(model, args.user_data)
        if user_data:
            logger.info(f"User data sample: {json.dumps({k: user_data[k] for k in list(user_data.keys())[:3]}, indent=2)}")
    
    elif args.test_mode == "job-details":
        job_details, _ = test_job_details_extraction(model, args.job_url)
        if job_details:
            logger.info(f"Job details sample: {json.dumps({k: job_details[k] for k in list(job_details.keys())[:3]}, indent=2)}")
    
    elif args.test_mode == "resume" or args.test_mode == "cover-letter":
        # First get the necessary data
        user_data = test_user_data_extraction(model, args.user_data)
        job_details, _ = test_job_details_extraction(model, args.job_url)
        
        if not user_data or not job_details:
            logger.error("Cannot proceed without user data and job details")
            return
            
        if args.test_mode == "resume":
            test_resume_builder(model, job_details, user_data)
        else:  # cover-letter
            test_cover_letter_generator(model, job_details, user_data)
    
    else:  # full pipeline
        result = test_full_pipeline(model, args.job_url, args.user_data)
        if result["success"]:
            logger.info("All tests completed successfully!")
        else:
            logger.error("Tests failed. Check logs for details.")

if __name__ == "__main__":
    main()
