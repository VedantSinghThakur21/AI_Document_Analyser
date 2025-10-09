# AWS CLI Commands for S3 Integration Setup
# Run these commands from your local machine where AWS CLI is configured

echo "🔐 Setting up IAM Role for EC2 S3 Access..."

# 1. Create IAM role for EC2 to access S3
echo "Creating IAM role: EC2-DocumentAnalyzer-S3-Role"
aws iam create-role \
  --role-name EC2-DocumentAnalyzer-S3-Role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }'

# 2. Create and attach the S3 policy
echo "Creating S3 policy: DocumentAnalyzer-S3-Policy"
aws iam create-policy \
  --policy-name DocumentAnalyzer-S3-Policy \
  --policy-document file://backend/s3-policy.json

# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 3. Attach the policy to the role
echo "Attaching policy to role..."
aws iam attach-role-policy \
  --role-name EC2-DocumentAnalyzer-S3-Role \
  --policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/DocumentAnalyzer-S3-Policy

# 4. Create instance profile
echo "Creating instance profile..."
aws iam create-instance-profile \
  --instance-profile-name EC2-DocumentAnalyzer-S3-Profile

# 5. Add role to instance profile
echo "Adding role to instance profile..."
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-DocumentAnalyzer-S3-Profile \
  --role-name EC2-DocumentAnalyzer-S3-Role

# 6. Attach instance profile to your EC2 instance
echo "Attaching instance profile to EC2..."
# Get your EC2 instance ID (replace with your actual instance ID)
INSTANCE_ID="i-0123456789abcdef0"  # REPLACE WITH YOUR ACTUAL INSTANCE ID

aws ec2 associate-iam-instance-profile \
  --instance-id ${INSTANCE_ID} \
  --iam-instance-profile Name=EC2-DocumentAnalyzer-S3-Profile

echo "✅ IAM setup complete!"
echo ""
echo "📋 Summary:"
echo "  - Created role: EC2-DocumentAnalyzer-S3-Role"
echo "  - Created policy: DocumentAnalyzer-S3-Policy"  
echo "  - Created instance profile: EC2-DocumentAnalyzer-S3-Profile"
echo "  - Attached to EC2 instance: ${INSTANCE_ID}"
echo ""
echo "⏳ Wait 2-3 minutes for IAM propagation, then deploy the backend"
echo ""
echo "🚀 Next steps:"
echo "  1. SSH to your EC2 instance"
echo "  2. Upload the enhanced backend files"
echo "  3. Run: bash deploy_enhanced_backend_with_s3.sh"

# Free Tier monitoring commands
echo ""
echo "📊 Free Tier Monitoring Commands:"
echo ""
echo "# Check S3 usage:"
echo "aws s3 ls s3://my-doc-analyzer-bucket-939404560/ --recursive --human-readable --summarize"
echo ""
echo "# Monitor monthly costs:"
echo "aws ce get-cost-and-usage --time-period Start=2024-10-01,End=2024-10-31 --granularity MONTHLY --metrics BlendedCost --group-by Type=DIMENSION,Key=SERVICE"