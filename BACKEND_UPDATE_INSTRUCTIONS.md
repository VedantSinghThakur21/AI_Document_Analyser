# Manual Backend Update Instructions

## Current Status
Based on the error output, your EC2 backend is running from `/home/ec2-user/` directly (not in a `backend/` subdirectory).

## Quick Fix Steps:

### 1. Update the summarizer.py file on EC2:
```bash
# On your EC2 instance, replace the current summarizer.py with our enhanced version
# You can either:

# Option A: Copy from your local machine (if you have SSH/SCP access)
scp -i "path/to/key.pem" backend/model/summarizer.py ec2-user@13.232.16.226:/home/ec2-user/model/

# Option B: Create the enhanced file directly on EC2
nano model/summarizer.py
# Then paste the contents of our enhanced summarizer.py
```

### 2. Install NLTK sentiment data:
```bash
# On EC2, run:
python3 -c "import nltk; nltk.download('vader_lexicon', quiet=True)"
```

### 3. Restart the backend service:
```bash
# Kill current process
pkill -f "uvicorn"

# Start enhanced backend
nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

### 4. Verify it's working:
```bash
curl http://localhost:8000/
```

## Alternative: Quick Test
Since the frontend is already updated with enhanced display capabilities, you can test the new features even with the current backend. The frontend will gracefully handle missing data fields.

## Current Frontend Features Working:
✅ Fixed double-upload issue
✅ Moved HTTPS banner (less intrusive)  
✅ Enhanced UI with new sections ready for enhanced analysis data

The enhanced analysis features will show up once the backend is updated with the new summarizer.py file.