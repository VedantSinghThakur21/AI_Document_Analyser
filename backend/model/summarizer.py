import logging
import nltk
import textstat
import re
from typing import Dict, List
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK data (lightweight)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
    logger.info("NLTK initialized successfully")
except Exception as e:
    logger.error(f"Error initializing NLTK: {str(e)}")

def simple_summarize(text: str, max_sentences: int = 3) -> str:
    """
    Create a simple extractive summary by selecting key sentences.
    """
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences by word frequency
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        word_freq = Counter([word for word in words if word.isalpha() and word not in stop_words])
        
        sentence_scores = {}
        for sentence in sentences:
            words_in_sentence = word_tokenize(sentence.lower())
            sentence_scores[sentence] = sum(word_freq[word] for word in words_in_sentence if word in word_freq)
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
        summary = ' '.join([sentence for sentence, score in top_sentences])
        return summary
    except:
        return text[:500] + "..." if len(text) > 500 else text

def extract_basic_entities(text: str) -> List[Dict]:
    """
    Extract basic named entities using NLTK.
    """
    try:
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        chunks = ne_chunk(pos_tags, binary=False)
        
        entities = []
        for chunk in chunks:
            if hasattr(chunk, 'label'):
                entity_text = ' '.join([token for token, pos in chunk.leaves()])
                entities.append({
                    "entity_group": chunk.label(),
                    "word": entity_text,
                    "score": 0.8  # Fixed score for NLTK entities
                })
        return entities
    except:
        return []

def analyze_text(text: str) -> dict:
    """
    Analyze text using lightweight NLP tools.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary containing summary and entities
    """
    try:
        # Truncate text to maximum 2000 characters for free tier
        truncated_text = text[:2000] if len(text) > 2000 else text
        logger.info(f"Processing text of length: {len(truncated_text)} characters")
        
        # Generate simple summary
        logger.info("Generating summary...")
        summary = simple_summarize(truncated_text)
        logger.info("Summary generated successfully")
        
        # Extract basic entities
        logger.info("Extracting named entities...")
        entities = extract_basic_entities(truncated_text)
        logger.info(f"Extracted {len(entities)} entities")
        
        # Add basic text statistics
        stats = {
            "word_count": len(truncated_text.split()),
            "sentence_count": len(sent_tokenize(truncated_text)),
            "readability_score": textstat.flesch_reading_ease(truncated_text)
        }
        
        return {
            "summary": summary,
            "entities": entities,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}")
        return {
            "summary": f"Error during analysis: {str(e)}",
            "entities": [],
            "statistics": {}
        }