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

echo "Step 3: Cloning repository..."
cd $INSTALL_DIR
if [ -d "$PROJECT_DIR" ]; then
    echo "Project directory already exists. Removing and re-cloning..."
    rm -rf $PROJECT_DIR
fi
git clone $REPO_URL $PROJECT_DIR

echo "Step 4: Navigating to project directory..."
cd $PROJECT_DIR

echo "Step 5: Creating Python virtual environment..."
python3 -m virtualenv venv

echo "Step 6: Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "========================================="
echo "Server setup completed successfully!"
echo "========================================="
echo ""
echo "Next manual steps:"
echo "1. cd $INSTALL_DIR/$PROJECT_DIR"
echo "2. source venv/bin/activate"
echo "3. cd backend"
echo "4. uvicorn app:app --host 0.0.0.0 --port 8000"
echo ""
echo "Your FastAPI server will be available at:"
echo "http://YOUR_SERVER_IP:8000"
echo ""
echo "Don't forget to:"
echo "- Update your security group to allow inbound traffic on port 8000"
echo "- Replace REPO_URL in this script with your actual repository URL"
echo "========================================="