#!/bin/bash

# Enhanced Backend Deployment with S3 Integration
# Deploy this on your EC2 instance

echo "🚀 Deploying Enhanced Backend with S3 Storage..."

# Update system packages
sudo yum update -y

# Install Python 3 and pip if not already installed
sudo yum install -y python3 python3-pip

# Install required Python packages
echo "📦 Installing Python dependencies..."
pip3 install --user fastapi uvicorn pdfplumber nltk textstat boto3

# Download NLTK data
python3 -c "
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nltk.download('vader_lexicon', quiet=True)
print('NLTK data downloaded successfully')
"

# Configure AWS credentials (EC2 instance should have IAM role)
echo "🔐 Configuring AWS credentials..."
aws configure set region ap-south-1
aws configure set output json

# Test S3 access
echo "🪣 Testing S3 bucket access..."
aws s3 ls s3://my-doc-analyzer-bucket-939404560/ || echo "⚠️ S3 access may need IAM role configuration"

# Create application directory if it doesn't exist
mkdir -p ~/backend/model

# Copy application files (you need to upload these first)
echo "📁 Application files should be in ~/backend/"
echo "Required files:"
echo "  - app.py (main FastAPI application)"
echo "  - model/summarizer.py (enhanced text analysis)"
echo "  - requirements.txt (optional)"

# Stop existing backend if running
echo "🛑 Stopping existing backend..."
pkill -f "uvicorn" || echo "No existing backend running"

# Start the enhanced backend with S3 integration
echo "🌟 Starting enhanced backend with S3 storage..."
cd ~/backend
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# Wait a moment and check if it's running
sleep 3
if pgrep -f "uvicorn" > /dev/null; then
    echo "✅ Backend started successfully!"
    echo "📊 Health check: curl http://localhost:8000/"
    echo "📝 Logs: tail -f ~/backend/backend.log"
else
    echo "❌ Backend failed to start. Check logs: cat ~/backend/backend.log"
fi

echo "🎯 Features enabled:"
echo "  ✅ PDF text extraction and analysis"
echo "  ✅ Named Entity Recognition (NER)"
echo "  ✅ Sentiment analysis with VADER"
echo "  ✅ Document classification"
echo "  ✅ Readability metrics"
echo "  ✅ S3 storage for PDFs and results"
echo "  ✅ Free Tier safeguards (10MB limit, 100 uploads/month)"

echo "🔍 Verify deployment:"
echo "  curl http://localhost:8000/"
echo "  curl -X POST -F 'file=@sample.pdf' http://localhost:8000/analyze"