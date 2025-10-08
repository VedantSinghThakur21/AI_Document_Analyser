import logging
from transformers import pipeline
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize models with error handling
try:
    logger.info("Loading summarization model...")
    summarizer = pipeline("summarization", model="t5-small")
    logger.info("Summarization model loaded successfully")
    
    logger.info("Loading NER model...")
    ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)
    logger.info("NER model loaded successfully")
    
except Exception as e:
    logger.error(f"Error loading models: {str(e)}")
    summarizer = None
    ner_model = None

def analyze_text(text: str) -> dict:
    """
    Analyze text using Hugging Face transformers for summarization and NER.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary containing summary and entities
    """
    try:
        # Check if models are loaded
        if summarizer is None or ner_model is None:
            logger.error("Models not properly loaded")
            return {
                "summary": "Error: Models not available",
                "entities": []
            }
        
        # Truncate text to maximum 1024 characters
        truncated_text = text[:1024] if len(text) > 1024 else text
        logger.info(f"Processing text of length: {len(truncated_text)} characters")
        
        # Generate summary
        logger.info("Generating summary...")
        summary_result = summarizer(truncated_text, max_length=150, min_length=30, do_sample=False)
        summary = summary_result[0]['summary_text'] if summary_result else "No summary generated"
        logger.info("Summary generated successfully")
        
        # Extract named entities
        logger.info("Extracting named entities...")
        ner_results = ner_model(truncated_text)
        
        # Format entities into clean list of dictionaries
        entities = []
        for entity in ner_results:
            formatted_entity = {
                "entity_group": entity["entity_group"],
                "word": entity["word"],
                "score": round(entity["score"], 3)
            }
            entities.append(formatted_entity)
        
        logger.info(f"Extracted {len(entities)} entities")
        
        return {
            "summary": summary,
            "entities": entities
        }
        
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}")
        return {
            "summary": f"Error during analysis: {str(e)}",
            "entities": []
        }