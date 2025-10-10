#!/bin/bash
set -e

# Configuration
BUCKET_NAME="doc-analyzer-$(date +%s)"  # Unique bucket name with timestamp
REGION="ap-south-1"
ACCOUNT_ID="073615522454"

echo "🪣 Creating new S3 bucket: $BUCKET_NAME"

# Create the bucket
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Create bucket folders
echo "📁 Creating bucket structure..."
aws s3api put-object --bucket $BUCKET_NAME --key uploads/ --region $REGION
aws s3api put-object --bucket $BUCKET_NAME --key results/ --region $REGION

# Set bucket policy (allows your account root and EC2S3ICC role)
echo "🔐 Setting bucket policy..."
cat > /tmp/bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowAccountAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::${ACCOUNT_ID}:root",
                    "arn:aws:iam::${ACCOUNT_ID}:role/EC2S3ICC"
                ]
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::${BUCKET_NAME}",
                "arn:aws:s3:::${BUCKET_NAME}/*"
            ]
        }
    ]
}
EOF

# Apply bucket policy
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file:///tmp/bucket-policy.json --region $REGION

# Enable versioning (optional)
aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled --region $REGION

# Set server-side encryption
aws s3api put-bucket-encryption --bucket $BUCKET_NAME --server-side-encryption-configuration '{
    "Rules": [
        {
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }
    ]
}' --region $REGION

# Clean up temp file
rm -f /tmp/bucket-policy.json

echo "✅ S3 bucket created successfully!"
echo ""
echo "📋 Bucket Details:"
echo "  Name: $BUCKET_NAME"
echo "  Region: $REGION"
echo "  Folders: uploads/, results/"
echo ""
echo "🔧 Next steps:"
echo "1. Update your backend app.py with the new bucket name"
echo "2. Test upload/download functionality"
echo ""
echo "💡 To update backend:"
echo "   sed -i 's/my-doc-analyzer-bucket-939404560/$BUCKET_NAME/g' backend/app.py"