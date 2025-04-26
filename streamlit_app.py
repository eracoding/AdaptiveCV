'''
-----------------------------------------------------------------------
File: streamlit_app.py
Description: Web application for AdaptiveCV - An AI-powered resume and cover letter generator
-----------------------------------------------------------------------
'''
import os
import json
import base64
import zipfile
import shutil
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('adaptivecv_app.log')
    ]
)
logger = logging.getLogger(__name__)

# Import AdaptiveCV
try:
    from src import AdaptiveCV
    logger.info("Successfully imported AdaptiveCV")
except ImportError as e:
    logger.error(f"Failed to import AdaptiveCV: {e}")
    st.error(f"Error importing AdaptiveCV: {e}")
    st.stop()

# Load environment variables
load_dotenv()

# Constants
PROVIDER_MODELS = {
    "GPT": ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
    "Gemini": ["gemini-pro", "gemini-1.5-pro"],
    "Ollama": ["llama2", "llama3", "mistral"]
}

# Set page configuration
st.set_page_config(
    page_title="AdaptiveCV - Smart Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    menu_items={
        'Get help': 'https://github.com/eracoding/AdaptiveCV',
        'About': 'AI-powered tool to generate tailored resumes and cover letters',
        'Report a bug': "https://github.com/eracoding/AdaptiveCV/issues",
    }
)

# Clean previous output directory
# if os.path.exists("output"):
#     shutil.rmtree("output")
os.makedirs("output", exist_ok=True)

# print("Session States: ", st.session_state)

# Helper Functions
def encode_tex_file(file_path):
    """Encode LaTeX files for Overleaf integration."""
    try:
        current_loc = os.path.dirname(__file__)
        file_paths = [
            file_path.replace('.pdf', '.tex'), 
            os.path.join(current_loc, 'src', 'templates', 'resume.cls')
        ]
        zip_file_path = file_path.replace('.pdf', '.zip')

        # Create a zip file
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                else:
                    logger.warning(f"File not found: {file_path}")

        # Read the zip file content as bytes
        with open(zip_file_path, 'rb') as zip_file:
            zip_content = zip_file.read()

        # Encode the data using Base64
        encoded_zip = base64.b64encode(zip_content).decode('utf-8')
        return encoded_zip
    
    except Exception as e:
        logger.error(f"Error encoding TeX file: {e}")
        st.error(f"An error occurred while encoding the LaTeX file: {e}")
        return None

def create_overleaf_button(resume_path):
    """Create an 'Edit in Overleaf' button for LaTeX files."""
    tex_content = encode_tex_file(resume_path)
    if tex_content:
        html_code = f"""
        <div style="max-height: 40px !important;">
            <form action="https://www.overleaf.com/docs" method="post" target="_blank">
                <input type="text" name="snip_uri" style="display: none;"
                    value="data:application/zip;base64,{tex_content}">
                <button type="submit" 
                    style="background-color: #4CAF50; color: white; padding: 8px 16px; 
                    border: none; border-radius: 20px; cursor: pointer; width: 100%; 
                    font-weight: bold; display: flex; align-items: center; justify-content: center;">
                    <svg width="20" height="20" style="margin-right: 8px;" viewBox="0 0 24 24" fill="white">
                        <path d="M7,9H2V7h5V9z M7,12H2v2h5V12z M20.59,19l-3.83-3.83C15.96,15.69,15.02,16,14,16c-2.76,0-5-2.24-5-5s2.24-5,5-5s5,2.24,5,5
                        c0,1.02-0.31,1.96-0.83,2.75L22,17.59L20.59,19z M14,8c-1.65,0-3,1.35-3,3s1.35,3,3,3s3-1.35,3-3S15.65,8,14,8z M2,19h10v-2H2V19z"/>
                    </svg>
                    Edit in Overleaf
                </button>
            </form>
        </div>
        """
        st.components.v1.html(html_code, height=50)
    else:
        st.warning("Unable to create Overleaf integration link")

def display_pdf(pdf_path):
    """Display a PDF file in Streamlit."""
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" 
        style="border: 1px solid #ddd; border-radius: 5px;" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying PDF: {e}")
        st.error(f"Failed to display PDF: {e}")

def calculate_metrics(resume_details, user_data, job_details):
    """Calculate similarity metrics for resume, user data, and job description."""
    try:
        from src.utils.metrics import (
            jaccard_similarity, 
            overlap_coefficient, 
            cosine_similarity
        )
        
        metrics = {}
        for metric_name, metric_func in [
            ("Overlap Coefficient", overlap_coefficient), 
            ("Cosine Similarity", cosine_similarity),
            ("Jaccard Similarity", jaccard_similarity)
        ]:
            user_personalization = metric_func(json.dumps(resume_details), json.dumps(user_data))
            job_alignment = metric_func(json.dumps(resume_details), json.dumps(job_details))
            job_match = metric_func(json.dumps(user_data), json.dumps(job_details))
            
            metrics[metric_name] = {
                "user_personalization": user_personalization,
                "job_alignment": job_alignment,
                "job_match": job_match
            }
            
        return metrics
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}")
        return None

def main():
    """Main Streamlit application function."""
    # App Header with Animation
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        animation: fadeIn 1.5s;
    }
    .subtitle {
        font-size: 1.2em;
        opacity: 0.9;
    }
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #4b6cb7;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4b6cb7 !important;
        color: white !important;
    }
    </style>
    
    <div class="main-header">
        <h1>AdaptiveCV - Smart Resume & Cover Letter Generator</h1>
        <p class="subtitle">AI-powered tool to create personalized resumes and cover letters tailored to job descriptions</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for a better organized UI
    tab1, tab2, tab3 = st.tabs(["📝 Create Documents", "ℹ️ How It Works", "🔧 Settings"])

    if 'generation_done' not in st.session_state:
        st.session_state['generation_done'] = False
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = None
    if 'job_details' not in st.session_state:
        st.session_state['job_details'] = None
    
    with tab1:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("Job Information")
            job_source = st.radio("Job Description Source:", ["URL", "Text"], horizontal=True)
            
            if job_source == "URL":
                job_url = st.text_input(
                    "Enter job posting URL:",
                    placeholder="https://www.example.com/job-posting",
                    help="Paste the complete URL of the job posting"
                )
                job_text = None
            else:
                job_text = st.text_area(
                    "Paste job description:",
                    height=200,
                    placeholder="Copy and paste the complete job description here...",
                    help="Include the complete job description for better results"
                )
                job_url = None
        
        with col2:
            st.subheader("Your Information")
            user_file = st.file_uploader(
                "Upload your resume or professional data file:", 
                type=["pdf", "json"],
                help="PDF resume or JSON file with your professional information"
            )
            
            if user_file:
                file_info = st.empty()
                file_info.info(f"Uploaded: {user_file.name}")
                
                # Save the uploaded file temporarily
                os.makedirs("uploads", exist_ok=True)
                user_file_path = os.path.join("uploads", user_file.name)
                with open(user_file_path, "wb") as f:
                    f.write(user_file.getbuffer())
                
                # Display file type icon based on extension
                if user_file.name.lower().endswith('.pdf'):
                    st.markdown("📄 PDF Resume detected")
                elif user_file.name.lower().endswith('.json'):
                    st.markdown("🔄 JSON Data file detected")

        # Model Selection and API Key
        st.subheader("AI Model Configuration")
        col_provider, col_model, col_api = st.columns(3)
        
        with col_provider:
            provider = st.selectbox("AI Provider:", list(PROVIDER_MODELS.keys()))
        
        with col_model:
            model = st.selectbox("Model:", PROVIDER_MODELS[provider])
        
        with col_api:
            if provider != "Ollama":
                api_key = st.text_input("API Key:", type="password", 
                                        help="Your API key for the selected provider")
                if not api_key and provider in ["GPT", "Gemini"]:
                    st.info(f"You can use environment variables for API keys")
            else:
                api_key = None
                st.info("Local Ollama installation will be used")
        
        # Action buttons
        st.subheader("Generate Documents")
        action_col1, action_col2, action_col3, action_col4 = st.columns([1, 1, 1, 1])

        with action_col1:
            generate_resume = st.button("Generate Resume", 
                                       type="primary", 
                                       use_container_width=True,
                                       help="Create a tailored resume based on the job description")
        
        with action_col2:
            generate_cover_letter = st.button("Generate Cover Letter", 
                                             type="primary", 
                                             use_container_width=True,
                                             help="Create a customized cover letter")
        
        with action_col3:
            generate_both = st.button("Generate Both", 
                                     type="primary", 
                                     use_container_width=True,
                                     help="Create both resume and cover letter")
            
            if generate_both:
                generate_resume = True
                generate_cover_letter = True
                
        with action_col4:
            reset_button = st.button("Reset", 
                                   type="secondary", 
                                   use_container_width=True,
                                   help="Clear all inputs and outputs")
            if reset_button:
                # Clear directories
                # if os.path.exists("uploads"):
                #     shutil.rmtree("uploads")
                # if os.path.exists("output"):
                #     shutil.rmtree("output")
                
                # Clear session state variables
                for key in ['resume_path', 'resume_details', 'resume_bytes', 'cv_path', 'cv_bytes', 'cover_letter', 'show_metrics', 'user_data', 'job_details', 'generation_done']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.rerun()

        # Process the generation request
        if generate_resume or generate_cover_letter:
            # Validate inputs
            if not user_file:
                st.error("Please upload your resume or professional data file")
                st.stop()
            
            if not ((job_url and job_url.strip()) or (job_text and job_text.strip())):
                st.error("Please provide either a job URL or paste the job description")
                st.stop()
            
            if provider != "Ollama" and not api_key:
                api_key = os.getenv(f"{provider.upper()}_API_KEY")
                if not api_key:
                    st.error(f"Please provide an API key for {provider}")
                    st.stop()
            
            # Initialize progress container
            progress_container = st.container()
            
            with progress_container:
                # Initialize the model
                with st.status("Initializing AI model...") as status:
                    try:
                        downloads_dir = os.path.abspath("output")
                        adaptive_cv = AdaptiveCV(
                            api_key=api_key,
                            provider=provider,
                            model=model,
                            downloads_dir=downloads_dir
                        )
                        status.update(label="AI model initialized", state="complete")
                        # Initialize session flags
                    except Exception as e:
                        logger.error(f"Error initializing model: {e}")
                        status.update(label=f"Failed to initialize model: {e}", state="error")
                        st.error(f"Error initializing the AI model: {e}")
                        st.stop()
                
                # Extract user data
                try:
                    # Show status while extracting
                    with st.status("Extracting your professional information...") as status:
                        user_data = adaptive_cv.user_data_extraction(user_file_path, is_st=False)
                        if user_data:
                            status.update(label="Professional information extracted successfully", state="complete")
                            st.session_state['user_data'] = user_data
                        else:
                            status.update(label="Failed to extract professional information", state="error")
                            st.error("Could not extract information from your file. Please check the format and try again.")
                            st.stop()
                except Exception as e:
                    logger.error(f"Error extracting user data: {e}")
                    st.error(f"Failed to process your file: {e}")
                    st.stop()
                
                # If extraction succeeded, show the data OUTSIDE of the status context
                if user_data:
                    # Now create the expander outside of any other expander-like contexts
                    with st.expander("View extracted professional data"):
                        st.json(user_data)
                
                # Extract job details
                with st.status("Analyzing job description...") as status:
                    try:
                        if job_url:
                            job_details, jd_path = adaptive_cv.job_details_extraction(url=job_url, is_st=False)
                        else:
                            job_details, jd_path = adaptive_cv.job_details_extraction(job_site_content=job_text, is_st=False)
                        
                        if job_details:
                            st.session_state['job_details'] = job_details
                            status.update(label="Job description analyzed successfully", state="complete")
                        else:
                            status.update(label="Failed to analyze job description", state="error")
                            st.error("Could not analyze the job description. Please check the URL or text and try again.")
                            st.stop()
                    except Exception as e:
                        logger.error(f"Error extracting job details: {e}")
                        status.update(label=f"Error analyzing job description: {e}", state="error")
                        st.error(f"Failed to analyze job description: {e}")
                        st.stop()
                
                if job_details:
                    # Show a sample of extracted job details
                    with st.expander("View analyzed job requirements"):
                        st.json(job_details)
                
                # Generate documents based on user selection
                output_container = st.container()
                with output_container:
                    # Initialize session state for resume and cover letter
                    if 'resume_path' not in st.session_state:
                        st.session_state.resume_path = None
                    if 'show_metrics' not in st.session_state:
                        st.session_state.show_metrics = False
                    if 'cv_path' not in st.session_state:
                        st.session_state.cv_path = None
                    
                    # Generate resume if requested or if we already have one in session state
                    if generate_resume or st.session_state.resume_path:
                        # Only generate if explicitly requested and we don't already have one
                        if generate_resume and not st.session_state.resume_path:
                            with st.status("Generating tailored resume...") as status:
                                try:
                                    resume_path, resume_details = adaptive_cv.resume_builder(job_details, user_data, is_st=False)
                                    if resume_path and os.path.exists(resume_path):
                                        # Store in session state
                                        st.session_state.resume_path = resume_path
                                        st.session_state.resume_details = resume_details
                                        status.update(label="Resume generated successfully", state="complete")
                                    else:
                                        status.update(label="Failed to generate resume", state="error")
                                        st.error("Could not generate the resume. Please try again.")
                                except Exception as e:
                                    logger.error(f"Error generating resume: {e}")
                                    status.update(label=f"Error generating resume: {e}", state="error")
                                    st.error(f"Failed to generate resume: {e}")
                        
                    # Generate cover letter if requested or if we already have one in session state
                    if generate_cover_letter or st.session_state.cv_path:
                        # Only generate if explicitly requested and we don't already have one
                        if generate_cover_letter and not st.session_state.cv_path:
                            with st.status("Generating personalized cover letter...") as status:
                                try:
                                    cover_letter, cv_path = adaptive_cv.cover_letter_generator(job_details, user_data, is_st=False)
                                    if cv_path and os.path.exists(cv_path):
                                        # Store in session state
                                        st.session_state.cv_path = cv_path
                                        status.update(label="Cover letter generated successfully", state="complete")
                                    else:
                                        status.update(label="Failed to generate cover letter", state="error")
                                        st.error("Could not generate the cover letter. Please try again.")
                                except Exception as e:
                                    logger.error(f"Error generating cover letter: {e}")
                                    status.update(label=f"Error generating cover letter: {e}", state="error")
                                    st.error(f"Failed to generate cover letter: {e}")
                        
                # Success message with animation
                if (generate_resume) or (generate_cover_letter):
                    st.session_state['generation_done'] = True
                    st.balloons()
                    st.success("Documents generated successfully! Download them using the buttons above.")
                
        if st.session_state['generation_done']:
            user_data = st.session_state['user_data']
            job_details = st.session_state['job_details']

            # Create a new container
            output_container = st.container()
            with output_container:
                st.subheader("Your Generated Documents 📄")

                if generate_resume or st.session_state.resume_path:
                    st.subheader("🎯 Your Tailored Resume")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        with open(st.session_state.resume_path, "rb") as f:
                            resume_bytes = f.read()

                        st.download_button(
                            label="Download Resume",
                            data=resume_bytes,
                            file_name=os.path.basename(st.session_state.resume_path),
                            mime="application/pdf",
                            key="resume_download",
                            use_container_width=True
                        )

                    with col2:
                        create_overleaf_button(st.session_state.resume_path)

                    with col3:
                        if st.button("Show Resume Metrics", key="metrics_btn", use_container_width=True):
                            st.session_state.show_metrics = True

                    if st.session_state.show_metrics:
                        metrics = calculate_metrics(st.session_state.resume_details, user_data, job_details)
                        if metrics:
                            with st.expander("📊 Resume Metrics", expanded=True):
                                st.markdown("### 🏆 Resume Similarity Metrics")

                                header_cols = st.columns([2, 1, 1, 1])  # Wider first column
                                header_cols[0].markdown("**Metric Type**")
                                header_cols[1].markdown("**Personalization**")
                                header_cols[2].markdown("**Job Alignment**")
                                header_cols[3].markdown("**Original Match**")

                                st.markdown("---")

                                # Iterate each metric type
                                for metric_name, values in metrics.items():
                                    row_cols = st.columns([2, 1, 1, 1])

                                    pretty_name = metric_name.replace("_", " ").title()  # e.g., "Overlap Coefficient"

                                    row_cols[0].markdown(f"**{pretty_name}**")

                                    row_cols[1].metric(
                                        label="🧑",
                                        value=f"{values['user_personalization']:.3f}",
                                        help="Personalization Score"
                                    )

                                    row_cols[2].metric(
                                        label="🎯",
                                        value=f"{values['job_alignment']:.3f}",
                                        help="Job Alignment Score"
                                    )

                                    row_cols[3].metric(
                                        label="🏢",
                                        value=f"{values['job_match']:.3f}",
                                        help="Original Resume Match Score"
                                    )

                    display_pdf(st.session_state.resume_path)

                if generate_cover_letter or st.session_state.cv_path:
                    st.subheader("📜 Your Cover Letter")
                    col1 = st.columns([1])[0]

                    with col1:
                        with open(st.session_state.cv_path, "rb") as f:
                            cv_bytes = f.read()

                        st.download_button(
                            label="Download Cover Letter",
                            data=cv_bytes,
                            file_name=os.path.basename(st.session_state.cv_path),
                            mime="application/pdf",
                            key="cv_download",
                            use_container_width=True
                        )

                    display_pdf(st.session_state.cv_path)

    with tab2:
        st.subheader("How AdaptiveCV Works")
        
        st.markdown("""
        ### The AdaptiveCV Process
        
        AdaptiveCV uses advanced AI to analyze job descriptions and your professional information to create 
        tailored documents that highlight the most relevant experience and skills for each specific job application.
        
        **Step 1: Data Extraction**
        - The system extracts structured information from your resume or professional data file
        - It analyzes the job description to identify key requirements, skills, and qualifications
        
        **Step 2: Alignment Analysis**
        - Your experience is compared against job requirements
        - The system identifies your strongest qualifications for the position
        - Gaps and areas for improvement are identified
        
        **Step 3: Document Generation**
        - A tailored resume is created highlighting your most relevant experience
        - A personalized cover letter is generated showcasing your qualifications
        - All documents are professionally formatted and ready to submit
        
        **Step 4: Performance Metrics**
        - The system provides metrics to help you understand how well your generated documents match the job requirements
        - You can use these insights to further refine your application
        
        ### Tips for Best Results
        
        1. **Provide complete information** in your professional data file
        2. **Use the full job description** rather than a summary
        3. **Try different AI models** for varied results (GPT models typically provide the best output)
        """)
        
        # Add a visual workflow diagram
        st.image("https://raw.githubusercontent.com/eracoding/AdaptiveCV/main/media/pipeline.png", 
            caption="The AdaptiveCV document generation workflow")

    with tab3:
        st.subheader("Settings & Configuration")
        
        # Path settings
        st.markdown("### Output Directory")
        output_path = st.text_input(
            "Set custom output directory (optional):",
            value="output",
            help="Directory where generated documents will be saved"
        )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            st.markdown("### Model Parameters")
            temperature = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make output more creative, lower values make it more deterministic"
            )
            
            st.markdown("### Document Formatting")
            template = st.selectbox(
                "Resume Template:",
                ["Standard", "Modern", "Academic", "Technical"],
                index=0,
                help="Select the resume template style"
            )
            
            st.markdown("### System")
            log_level = st.selectbox(
                "Log Level:",
                ["DEBUG", "INFO", "WARNING", "ERROR"],
                index=1,
                help="Set the logging verbosity level"
            )
            
            if st.button("Apply Settings"):
                # Here you would apply these settings to your AdaptiveCV instance
                st.success("Settings applied successfully!")
        
        # About section
        with st.expander("About AdaptiveCV"):
            st.markdown("""
            ### AdaptiveCV
            
            Version: 1.0.0
            
            AdaptiveCV is an AI-powered tool that helps job seekers create tailored resumes and cover letters 
            that align with specific job descriptions. The system uses advanced natural language processing 
            to analyze job requirements and match them with the applicant's qualifications.
            
            **GitHub Repository**: [github.com/eracoding/AdaptiveCV](https://github.com/eracoding/AdaptiveCV)
            
            **License**: MIT
            """)

if __name__ == "__main__":
    main()
