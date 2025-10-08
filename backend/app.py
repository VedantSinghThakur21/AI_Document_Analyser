import logging
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from model.summarizer import analyze_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Document Analyzer API", version="1.0.0")

# Configure CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Root endpoint for health check"""
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze uploaded PDF document
    """
    try:
        logger.info(f"Received file: {file.filename}")
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        file_content = await file.read()
        
        # Extract text from PDF using pdfplumber
        extracted_text = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
                logger.info(f"Processed page {page_num}")
        
        # Check if any text was extracted
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
        
        logger.info(f"Extracted {len(extracted_text)} characters from PDF")
        
        # Analyze the extracted text
        logger.info("Starting text analysis...")
        analysis_result = analyze_text(extracted_text)
        logger.info("Analysis complete")
        
        return {
            "status": "success",
            "data": analysis_result
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)