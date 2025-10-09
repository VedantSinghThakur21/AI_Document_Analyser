#!/bin/bash
# Enhanced Backend Deployment Script
# Run this on your EC2 instance after copying the enhanced summarizer.py

echo "🚀 Deploying Enhanced AI Document Analyzer Backend..."

# Navigate to backend directory
cd ~/AI_Document_Analyser/backend

# Check if enhanced summarizer exists
if [ -f "model/summarizer.py" ]; then
    echo "✅ Enhanced summarizer.py found"
    
    # Check file size (enhanced version should be larger)
    SIZE=$(wc -l < model/summarizer.py)
    if [ $SIZE -gt 100 ]; then
        echo "✅ Summarizer appears to be enhanced version ($SIZE lines)"
    else
        echo "⚠️  Summarizer might be basic version ($SIZE lines)"
    fi
else
    echo "❌ Enhanced summarizer.py not found!"
    echo "Please copy the enhanced summarizer.py to model/ directory"
    exit 1
fi

# Install required packages
echo "📦 Installing required Python packages..."
pip install nltk textstat

# Download NLTK data
echo "📚 Downloading NLTK data..."
python3 -c "
import nltk
print('Downloading NLTK data...')
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
print('✅ NLTK data downloaded successfully')
"

# Stop existing backend
echo "🔄 Stopping existing backend..."
pkill -f uvicorn 2>/dev/null || echo "No existing backend running"

# Start enhanced backend
echo "🚀 Starting enhanced backend..."
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 > nohup.out 2>&1 &

# Wait and test
sleep 5
echo "🔍 Testing backend..."
if curl -s http://localhost:8000/ | grep -q "ok"; then
    echo "✅ Enhanced backend is running successfully!"
    echo ""
    echo "🎉 Deployment Complete!"
    echo "Your AI Document Analyzer now supports:"
    echo "  ✅ Enhanced document summarization"
    echo "  ✅ Named entity extraction"
    echo "  ✅ Keyword analysis"
    echo "  ✅ Sentiment analysis"
    echo "  ✅ Document classification"
    echo "  ✅ Advanced readability metrics"
    echo ""
    echo "Test your app at:"
    echo "  HTTP:  http://vedantsinghthakur21.github.io/AI_Document_Analyser/"
    echo "  HTTPS: https://vedantsinghthakur21.github.io/AI_Document_Analyser/"
else
    echo "❌ Backend failed to start. Check nohup.out for errors:"
    tail -n 20 nohup.out
fi