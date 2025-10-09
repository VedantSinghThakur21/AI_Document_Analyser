#!/bin/bash
# Update backend with enhanced analysis

# Check current directory and show structure
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Find the backend files
if [ -d "backend" ]; then
    echo "Found backend directory"
    cd backend
elif [ -f "app.py" ]; then
    echo "Found app.py in current directory"
    # We're already in the right place
else
    echo "Looking for backend files..."
    find . -name "app.py" -type f 2>/dev/null | head -1
    find . -name "summarizer.py" -type f 2>/dev/null | head -1
fi

# Show current backend structure
echo "Backend structure:"
ls -la

# Backup current summarizer if it exists
if [ -f "model/summarizer.py" ]; then
    echo "Backing up existing summarizer..."
    cp model/summarizer.py model/summarizer.py.backup
elif [ -f "summarizer.py" ]; then
    echo "Backing up existing summarizer..."
    cp summarizer.py summarizer.py.backup
else
    echo "No existing summarizer found to backup"
fi

# Install additional NLTK data for sentiment analysis
echo "Installing NLTK data..."
python3 -c "
import nltk
try:
    nltk.download('vader_lexicon', quiet=True)
    print('VADER lexicon downloaded successfully')
except Exception as e:
    print(f'Error downloading VADER: {e}')
"

# Restart the backend service
echo "Restarting backend service..."
sudo pkill -f "uvicorn" 2>/dev/null || pkill -f "python.*app" 2>/dev/null
sleep 3

# Check if we have a virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the backend again
echo "Starting backend server..."
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# Wait a moment and check if it started
sleep 5
echo "Checking backend status..."
curl -s http://localhost:8000/ || echo "Backend not responding yet, check backend.log"

echo "Backend update completed!"
echo "Check logs with: tail -f backend.log"
echo "Check status with: curl http://localhost:8000/"