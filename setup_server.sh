 # This file has been removed as it is no longer needed.
#!/bin/bash
set -e

# Configuration variables
REPO_URL="https://github.com/VedantSinghThakur21/AI_Document_Analyser"
PROJECT_DIR="AI_Document_Analyser"
INSTALL_DIR="/home/ec2-user"

echo "========================================="
echo "Starting Amazon Linux Server Setup"
echo "========================================="

echo "Step 1: Updating package manager..."
sudo yum update -y

echo "Step 2: Installing required packages..."
sudo yum install -y python3-pip git
pip3 install virtualenv

echo "Step 3: Cleaning up previous installations (Free Tier Optimization)..."
rm -rf ~/.cache/pip
rm -rf ~/.cache/*
if [ -d "$INSTALL_DIR/$PROJECT_DIR" ]; then
    echo "Removing previous project directory..."
    rm -rf $INSTALL_DIR/$PROJECT_DIR
fi

echo "Step 4: Cloning repository..."
cd $INSTALL_DIR
git clone $REPO_URL

echo "Step 5: Navigating to project directory..."
cd $PROJECT_DIR

echo "Step 6: Creating Python virtual environment..."
python3 -m virtualenv venv

echo "Step 7: Activating virtual environment and installing lightweight dependencies..."
source venv/bin/activate
pip install --upgrade pip

echo "Step 8: Installing packages (optimized for free tier)..."
pip install -r requirements.txt

echo "Step 9: Checking disk usage after installation..."
df -h

echo "========================================="
echo "🎉 FREE TIER SERVER SETUP COMPLETED! 🎉"
echo "========================================="
echo ""
echo "✅ Lightweight NLP dependencies installed"
echo "✅ Virtual environment configured"
echo "✅ Ready to run your Document Analyzer!"
echo ""
echo "🚀 To start your FastAPI server:"
echo "1. cd $INSTALL_DIR/$PROJECT_DIR"
echo "2. source venv/bin/activate"
echo "3. cd backend"
echo "4. uvicorn app:app --host 0.0.0.0 --port 8000"
echo ""
echo "🌐 Your server will be available at:"
echo "   http://13.232.16.226:8000"
echo ""
echo "📝 API Endpoints:"
echo "   - GET  /          → Health check"
echo "   - POST /analyze   → Upload & analyze PDF"
echo ""
echo "⚠️  IMPORTANT REMINDERS:"
echo "   - Add security group rule for port 8000"
echo "   - Server optimized for AWS Free Tier"
echo "   - Uses lightweight NLTK instead of heavy ML models"
echo "========================================="