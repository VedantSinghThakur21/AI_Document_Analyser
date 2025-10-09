import logging
import nltk
import textstat
import re
from typing import Dict, List, Tuple
from collections import Counter
import string
from datetime import datetime

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
    nltk.download('vader_lexicon', quiet=True)
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
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

def extract_keywords(text: str, top_k: int = 10) -> List[Dict]:
    """
    Extract important keywords using TF-IDF-like scoring.
    """
    try:
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        
        # Filter words: alphabetic, not stopwords, length > 3
        filtered_words = [word for word in words if 
                         word.isalpha() and 
                         word not in stop_words and 
                         len(word) > 3]
        
        # Calculate word frequency
        word_freq = Counter(filtered_words)
        
        # Get top keywords with scores
        keywords = []
        total_words = len(filtered_words)
        for word, freq in word_freq.most_common(top_k):
            score = freq / total_words
            keywords.append({
                "word": word.title(),
                "frequency": freq,
                "score": round(score * 100, 2)  # Convert to percentage
            })
        
        return keywords
    except:
        return []

def analyze_sentiment(text: str) -> Dict:
    """
    Analyze sentiment using VADER sentiment analyzer.
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        
        # Determine overall sentiment
        if scores['compound'] >= 0.05:
            overall = "Positive"
            emoji = "😊"
        elif scores['compound'] <= -0.05:
            overall = "Negative"
            emoji = "😟"
        else:
            overall = "Neutral"
            emoji = "😐"
        
        return {
            "overall": overall,
            "emoji": emoji,
            "scores": {
                "positive": round(scores['pos'] * 100, 1),
                "negative": round(scores['neg'] * 100, 1),
                "neutral": round(scores['neu'] * 100, 1),
                "compound": round(scores['compound'], 3)
            }
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return {
            "overall": "Analysis unavailable",
            "emoji": "❓",
            "scores": {"positive": 0, "negative": 0, "neutral": 0, "compound": 0},
            "error": str(e)
        }

def classify_document_type(text: str) -> Dict:
    """
    Classify document type based on content patterns.
    """
    text_lower = text.lower()
    
    # Define patterns for different document types
    patterns = {
        "Academic Paper": [
            "abstract", "methodology", "conclusion", "references", 
            "hypothesis", "literature review", "data analysis"
        ],
        "Business Report": [
            "executive summary", "revenue", "profit", "quarterly", 
            "stakeholder", "roi", "kpi", "market analysis"
        ],
        "Legal Document": [
            "whereas", "hereby", "agreement", "contract", "clause", 
            "defendant", "plaintiff", "jurisdiction"
        ],
        "Technical Manual": [
            "installation", "configuration", "troubleshooting", 
            "specifications", "requirements", "procedure"
        ],
        "News Article": [
            "according to", "reported", "sources", "breaking", 
            "update", "journalist", "correspondent"
        ],
        "Marketing Material": [
            "discover", "exclusive", "limited time", "call now", 
            "special offer", "guarantee", "testimonial"
        ]
    }
    
    scores = {}
    for doc_type, keywords in patterns.items():
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        scores[doc_type] = matches
    
    if max(scores.values()) > 0:
        predicted_type = max(scores.keys(), key=lambda x: scores[x])
        confidence = scores[predicted_type] / len(patterns[predicted_type]) * 100
    else:
        predicted_type = "General Document"
        confidence = 0
    
    return {
        "type": predicted_type,
        "confidence": round(confidence, 1),
        "all_scores": scores
    }

def get_readability_metrics(text: str) -> Dict:
    """
    Get comprehensive readability metrics.
    """
    try:
        # Ensure we have enough text for meaningful analysis
        if len(text.strip()) < 50:
            return {
                "flesch_reading_ease": 0.0,
                "flesch_kincaid_grade": 0.0,
                "gunning_fog": 0.0,
                "automated_readability": 0.0,
                "coleman_liau": 0.0,
                "reading_level": "Text too short for analysis"
            }
        
        return {
            "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 1),
            "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 1),
            "gunning_fog": round(textstat.gunning_fog(text), 1),
            "automated_readability": round(textstat.automated_readability_index(text), 1),
            "coleman_liau": round(textstat.coleman_liau_index(text), 1),
            "reading_level": textstat.text_standard(text)
        }
    except Exception as e:
        logger.error(f"Error calculating readability metrics: {str(e)}")
        return {
            "flesch_reading_ease": 0.0,
            "flesch_kincaid_grade": 0.0,
            "gunning_fog": 0.0,
            "automated_readability": 0.0,
            "coleman_liau": 0.0,
            "reading_level": f"Analysis error: {str(e)}"
        }

def analyze_text(text: str) -> dict:
    """
    Comprehensive text analysis using lightweight NLP tools.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: Dictionary containing comprehensive analysis results
    """
    try:
        # Truncate text for processing efficiency (3000 chars for better analysis)
        truncated_text = text[:3000] if len(text) > 3000 else text
        logger.info(f"Processing text of length: {len(truncated_text)} characters")
        
        # 1. Generate summary
        logger.info("Generating summary...")
        summary = simple_summarize(truncated_text, max_sentences=4)
        
        # 2. Extract entities
        logger.info("Extracting named entities...")
        entities = extract_basic_entities(truncated_text)
        
        # 3. Extract keywords
        logger.info("Extracting keywords...")
        keywords = extract_keywords(truncated_text, top_k=8)
        
        # 4. Analyze sentiment
        logger.info("Analyzing sentiment...")
        sentiment = analyze_sentiment(truncated_text)
        
        # 5. Classify document type
        logger.info("Classifying document type...")
        doc_classification = classify_document_type(truncated_text)
        
        # 6. Get readability metrics
        logger.info("Calculating readability metrics...")
        readability = get_readability_metrics(truncated_text)
        
        # 7. Enhanced statistics
        sentences = sent_tokenize(truncated_text)
        words = word_tokenize(truncated_text)
        
        stats = {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len([p for p in truncated_text.split('\n\n') if p.strip()]),
            "character_count": len(truncated_text),
            "avg_words_per_sentence": round(len(words) / len(sentences), 1) if sentences else 0,
            "avg_sentence_length": round(len(truncated_text) / len(sentences), 1) if sentences else 0,
            "readability_score": readability["flesch_reading_ease"],
            "reading_level": readability["reading_level"]
        }
        
        logger.info("Analysis completed successfully")
        
        return {
            "summary": summary,
            "entities": entities,
            "keywords": keywords,
            "sentiment": sentiment,
            "document_type": doc_classification,
            "readability": readability,
            "statistics": stats,
            "analysis_timestamp": datetime.now().isoformat(),
            "text_length": len(text),
            "processed_length": len(truncated_text)
        }
        
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}")
        return {
            "summary": f"Error during analysis: {str(e)}",
            "entities": [],
            "keywords": [],
            "sentiment": {"overall": "Unknown", "emoji": "❓"},
            "document_type": {"type": "Unknown", "confidence": 0},
            "readability": {},
            "statistics": {},
            "analysis_timestamp": datetime.now().isoformat(),
            "error": str(e)
        }