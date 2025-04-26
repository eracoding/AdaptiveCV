'''
---------------------------------
File: llm_models.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
---------------------------------
'''
import json
import logging

from typing import Dict, List, Optional, Union, Any

import pandas as pd
import streamlit as st

from openai import OpenAI

from src.utils.utils import parse_json_markdown
from src.envs import GPT_EMBEDDING_MODEL


logger = logging.getLogger(__name__)

class ChatGPT:
    """
    A wrapper class for OpenAI's GPT models with simplified interface for 
    generating responses and embeddings.
    """
    def __init__(self, api_key: str, model: str, system_prompt: str):
        """
        Initialize the ChatGPT client.
        
        Args:
            api_key (str): OpenAI API key
            model (str): Model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
            system_prompt (str): System prompt/instruction to guide model behavior
        """
        self.model = model
        self.system_prompt = {"role": "system", "content": system_prompt.strip()} if system_prompt.strip() else None
        self.client = OpenAI(api_key=api_key)

    def get_response(self,
                     prompt: str,
                     expecting_longer_output: bool = False,
                     need_json_output: bool = False,
                     temperature: float = 0) -> Union[str, Dict[str, Any]]:
        """
        Get a response from the GPT model.
        
        Args:
            prompt (str): User input/prompt text
            expecting_longer_output (bool): Whether to allocate more tokens for longer responses
            need_json_output (bool): Whether to request and parse JSON output
            temperature (float): Sampling temperature (0-1), lower is more deterministic
            
        Returns:
            Union[str, Dict[str, Any]]: Plain text response or parsed JSON object
        """
        messages = []
        if self.system_prompt:
            messages.append(self.system_prompt)
        messages.append({"role": "user", "content": prompt})

        response_format = {"type": "json_object"} if need_json_output else None
        max_tokens = 4000 if expecting_longer_output else None

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )

            content = completion.choices[0].message.content.strip()

            if need_json_output:
                return parse_json_markdown(content) or {}
            return content
        
        except Exception as e:
            logger.error(f"Error in OpenAI API: {e}")
            st.error(f"Error in OpenAI API: {str(e)}")
            st.markdown("<h3 style='text-align: center;'>Please try again! Check the log in the dropdown for more details.</h3>", unsafe_allow_html=True)
            return {} if need_json_output else ""
        
    
    def get_embedding(self,
                      text: Union[str, List[str]],
                      model: str = GPT_EMBEDDING_MODEL,
                      task_type: str = 'retrieval_document') -> Union[List[float], pd.DataFrame]:
        """
        Generate embeddings for text using OpenAI's embedding models.
        
        Args:
            text (Union[str, List[str]]): Single text string or list of text chunks
            model (str): Embedding model to use
            task_type (str): Task type for embedding (only used for compatibility with other LLM classes)
            
        Returns:
            Union[List[float], pd.DataFrame]: Raw embedding vector or DataFrame with embeddings
        """
        try:
            if isinstance(text, list):
                df = pd.DataFrame(text, columns=['chunk'])

                df['chunk'] = df['chunk'].apply(lambda x: x.replace("\n", " ") if isinstance(x, str) else str(x))
                df['embedding'] = df['chunk'].apply(
                    lambda x: self.client.embeddings.create(input=[x], model=model).data[0].embedding
                )
                
                return df
            else:
                cleaned_text = text.replace("\n", " ") if isinstance(text, str) else str(text)
                return self.client.embeddings.create(input=[cleaned_text], model=model).data[0].embedding
        except Exception as e:
            logger.error(f"Error in getting embeddings: {e}")
            if isinstance(text, list):
                return pd.DataFrame(columns=['chunk', 'embedding'])
            return []

