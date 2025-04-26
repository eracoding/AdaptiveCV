'''
---------------------------------
File: metrics.py
Author: Ulugbek Shernazarov
Email: u.shernaz4rov@gmail.com
Copyright (c) 2025 Ulugbek Shernazarov. All rights reserved | GitHub: eracoding
---------------------------------
'''
import re
import json
import numpy as np
import pandas as pd

from typing import List, Dict, Any, Optional, Set
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

# nltk modules
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from src.utils.utils import key_value_chunking

# Downloading nltk resources
try:
    nltk.data.find('punkt_tab')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    nltk.data.find('corpora/stopwords')
except Exception as e:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('stopwords', quiet=True)


# Pre-compute common sets
STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()
URL_PATTERN = re.compile(r"https?://\S+")
NON_ALPHA_PATTERN = re.compile('[^a-zA-Z]')


def remove_urls(list_of_strings: List[str]) -> List[str]:
    """Remove strings containing URLs using re"""
    return [string for string in list_of_strings if not URL_PATTERN.search(string)]


@lru_cache(maxsize=128)
def normalize_text(text: str) -> List[str]:
    """Normalize the input text (tokenization, cleaning, stemming)
    
    Cached for performance when processing repeated text segments.
    
    Args:
        text (str): The text to normalize.
        
    Returns:
        List[str]: The list of normalized words.
    """

    words = word_tokenize(text)

    words = [
        STEMMER.stem(word)
        for word in (NON_ALPHA_PATTERN.sub('', word).lower() for word in words)
        if word and word not in STOP_WORDS
    ]

    return words


def _get_word_sets(document1: str, document2: str) -> tuple[Set[str], Set[str]]:
    """Helper function to get normalized word sets"""
    words1 = set(normalize_text(document1))
    words2 = set(normalize_text(document2))

    return words1, words2


def overlap_coefficient(document1: str, document2: str) -> float:
    """Calculate the overlap coefficient
    
    The overlap coefficient is defined as the size of the intersection 
    divided by the size of the smaller set.
    
    Args:
        document1 (str): The first document.
        document2 (str): The second document.
        
    Returns:
        float: The overlap coefficient between the two documents.
    """

    words1, words2 = _get_word_sets(document1, document2)

    min_size = min(len(words1), len(words2))
    if min_size == 0:
        return 0.0
    
    intersection_size = len(words1.intersection(words2))

    return intersection_size / min_size


def jaccard_similarity(document1: str, document2: str) -> float:
    """Calculate the Jaccard similarity between two documents.
    
    Defined as the size of the intersection divided by the size of the union.
    
    Args:
        document1 (str): The first document.
        document2 (str): The second document.
        
    Returns:
        float: The Jaccard similarity between the two documents.
    """
    words1, words2 = _get_word_sets(document1, document2)

    union_size = len(words1.union(words2))
    if union_size == 0:
        return 0.0
    
    intersection_size = len(words1.intersection(words2))

    return intersection_size / union_size


def cosine_similarity(document1: str, document2: str) -> float:
    """Calculate the cosine similarity between two documents using TF-IDF vectors.
    
    Args:
        document1 (str): The first document.
        document2 (str): The second document.
        
    Returns:
        float: The cosine similarity score between the documents.
    """

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([document1, document2])

    similarity = sklearn_cosine_similarity(vectors[0:1], vectors[1:2])[0, 0]
    return similarity


def vector_embedding_similarity(llm, document1: str, document2: str) -> float:
    """Calculate similarity between documents using vector embeddings.
    
    Args:
        llm: The language model to use for embeddings.
        document1 (str): The first document (JSON string).
        document2 (str): The second document (JSON string).
        
    Returns:
        float: The average cosine similarity between document embeddings.
    """

    doc1_chunks = key_value_chunking(json.loads(document1))
    doc2_chunks = key_value_chunking(json.loads(document2))

    emb_1 = llm.get_embedding(doc1_chunks, task_type="retrieval_query")
    emb_2 = llm.get_embedding(doc2_chunks, task_type="retrieval_query")

    df1 = pd.DataFrame(emb_1.embedding.to_list())
    df2 = pd.DataFrame(emb_2.embedding.to_list())

    similarity_matrix = pairwise.cosine_similarity(df1, df2)
    return similarity_matrix.mean()

