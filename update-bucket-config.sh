#!/bin/bash
# Update backend configuration for new S3 bucket

NEW_BUCKET_NAME="$1"
OLD_BUCKET_NAME="my-doc-analyzer-bucket-939404560"

if [ -z "$NEW_BUCKET_NAME" ]; then
    echo "❌ Usage: $0 <new-bucket-name>"
    echo "Example: $0 doc-analyzer-1728567890"
    exit 1
fi

echo "🔧 Updating backend configuration..."
echo "  Old bucket: $OLD_BUCKET_NAME"
echo "  New bucket: $NEW_BUCKET_NAME"

# Update app.py
if [ -f "backend/app.py" ]; then
    sed -i "s/$OLD_BUCKET_NAME/$NEW_BUCKET_NAME/g" backend/app.py
    echo "✅ Updated backend/app.py"
else
    echo "❌ backend/app.py not found"
fi

# Update s3-policy.json
if [ -f "backend/s3-policy.json" ]; then
    sed -i "s/$OLD_BUCKET_NAME/$NEW_BUCKET_NAME/g" backend/s3-policy.json
    echo "✅ Updated backend/s3-policy.json"
else
    echo "❌ backend/s3-policy.json not found"
fi

# Update deployment script
if [ -f "deploy_enhanced_backend_with_s3.sh" ]; then
    sed -i "s/$OLD_BUCKET_NAME/$NEW_BUCKET_NAME/g" deploy_enhanced_backend_with_s3.sh
    echo "✅ Updated deploy_enhanced_backend_with_s3.sh"
else
    echo "❌ deploy_enhanced_backend_with_s3.sh not found"
fi

# Update documentation
if [ -f "S3_INTEGRATION_GUIDE.md" ]; then
    sed -i "s/$OLD_BUCKET_NAME/$NEW_BUCKET_NAME/g" S3_INTEGRATION_GUIDE.md
    echo "✅ Updated S3_INTEGRATION_GUIDE.md"
else
    echo "❌ S3_INTEGRATION_GUIDE.md not found"
fi

echo ""
echo "✅ Backend configuration updated!"
echo "🔧 Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Update S3 bucket name to $NEW_BUCKET_NAME'"
echo "2. Deploy updated backend: bash deploy_enhanced_backend_with_s3.sh"
echo "3. Test the application"