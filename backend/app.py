import logging
import io
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from model.summarizer import analyze_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# S3 Configuration (Free Tier Compliant)
S3_BUCKET_NAME = "my-doc-analyzer-bucket-939404560"
S3_REGION = "ap-south-1"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit for Free Tier safety
MAX_MONTHLY_UPLOADS = 100  # Conservative limit for Free Tier

# Initialize S3 client
try:
    s3_client = boto3.client('s3', region_name=S3_REGION)
    logger.info("S3 client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize S3 client: {str(e)}")
    s3_client = None

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

def upload_to_s3(file_content: bytes, filename: str, content_type: str = "application/pdf") -> str:
    """
    Upload file to S3 bucket with Free Tier safeguards
    Returns S3 object key if successful, None if failed
    """
    if not s3_client:
        logger.error("S3 client not available")
        return None
    
    # Free Tier safety checks
    if len(file_content) > MAX_FILE_SIZE:
        logger.warning(f"File {filename} exceeds size limit: {len(file_content)} bytes")
        return None
    
    try:
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y/%m/%d/%H%M%S")
        s3_key = f"uploads/{timestamp}_{filename}"
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type,
            ServerSideEncryption='AES256'  # Free encryption
        )
        
        logger.info(f"Successfully uploaded {filename} to S3 as {s3_key}")
        return s3_key
        
    except ClientError as e:
        logger.error(f"Failed to upload {filename} to S3: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error uploading {filename}: {str(e)}")
        return None

def upload_analysis_results(results: dict, filename: str) -> str:
    """
    Upload analysis results as JSON to S3
    Returns S3 object key if successful, None if failed
    """
    if not s3_client:
        return None
    
    try:
        # Generate results filename
        timestamp = datetime.now().strftime("%Y/%m/%d/%H%M%S")
        base_name = filename.replace('.pdf', '').replace('.PDF', '')
        s3_key = f"results/{timestamp}_{base_name}_analysis.json"
        
        # Prepare results with metadata
        analysis_data = {
            "original_file": filename,
            "analysis_timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        # Upload JSON to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(analysis_data, indent=2),
            ContentType='application/json',
            ServerSideEncryption='AES256'
        )
        
        logger.info(f"Successfully uploaded analysis results to S3 as {s3_key}")
        return s3_key
        
    except Exception as e:
        logger.error(f"Failed to upload analysis results: {str(e)}")
        return None

@app.get("/")
async def health_check():
    """Root endpoint for health check with S3 status"""
    s3_status = "unavailable"
    
    if s3_client:
        try:
            # Test S3 connectivity
            s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
            s3_status = "connected"
        except Exception as e:
            s3_status = f"error: {str(e)}"
    
    return {
        "status": "ok",
        "s3_storage": s3_status,
        "bucket": S3_BUCKET_NAME,
        "features": ["pdf_upload", "text_analysis", "s3_storage"]
    }

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze uploaded PDF document and save to S3
    """
    try:
        logger.info(f"Received file: {file.filename}")
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        file_content = await file.read()
        
        # Free Tier safety check
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size allowed: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
        
        # Upload original PDF to S3 (async operation, don't block on failure)
        s3_pdf_key = None
        if s3_client:
            try:
                s3_pdf_key = upload_to_s3(file_content, file.filename, "application/pdf")
                if s3_pdf_key:
                    logger.info(f"PDF uploaded to S3: {s3_pdf_key}")
            except Exception as e:
                logger.warning(f"S3 upload failed but continuing with analysis: {str(e)}")
        
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
        
        # Upload analysis results to S3 (async operation, don't block on failure)
        s3_results_key = None
        if s3_client:
            try:
                s3_results_key = upload_analysis_results(analysis_result, file.filename)
                if s3_results_key:
                    logger.info(f"Analysis results uploaded to S3: {s3_results_key}")
            except Exception as e:
                logger.warning(f"Failed to upload analysis results to S3: {str(e)}")
        
        # Prepare response with S3 information
        response_data = {
            "status": "success",
            "data": analysis_result,
            "storage": {
                "pdf_uploaded": s3_pdf_key is not None,
                "results_uploaded": s3_results_key is not None,
                "pdf_s3_key": s3_pdf_key,
                "results_s3_key": s3_results_key
            }
        }
        
        return response_data
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/storage-stats")
async def get_storage_stats():
    """
    Get S3 storage statistics for Free Tier monitoring
    """
    if not s3_client:
        return {"error": "S3 client not available"}
    
    try:
        # List objects to get count and total size
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=S3_BUCKET_NAME)
        
        total_size = 0
        total_files = 0
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    total_size += obj['Size']
                    total_files += 1
        
        # Convert to human readable
        size_mb = total_size / (1024 * 1024)
        free_tier_limit_gb = 5
        usage_percent = (size_mb / (free_tier_limit_gb * 1024)) * 100
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(size_mb, 2),
            "free_tier_limit_gb": free_tier_limit_gb,
            "usage_percent": round(usage_percent, 2),
            "files_limit": MAX_MONTHLY_UPLOADS,
            "within_limits": size_mb < (free_tier_limit_gb * 1024) and total_files < MAX_MONTHLY_UPLOADS
        }
        
    except Exception as e:
        logger.error(f"Error getting storage stats: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)