#!/bin/bash
set -e

REGION=${1:-ap-south-1}
LOG_GROUP="/doc-analyzer/backend"

echo "🔧 Installing/Starting CloudWatch Agent in region ${REGION}..."

# Install CloudWatch Agent
sudo yum install -y amazon-cloudwatch-agent || true

# Create log group if not exists
aws logs describe-log-groups --log-group-name-prefix ${LOG_GROUP} --region ${REGION} | grep ${LOG_GROUP} >/dev/null 2>&1 || \
  aws logs create-log-group --log-group-name ${LOG_GROUP} --region ${REGION}

# Put a default retention policy (7 days)
aws logs put-retention-policy --log-group-name ${LOG_GROUP} --retention-in-days 7 --region ${REGION} || true

# Write config
sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json >/dev/null << 'EOF'
$(cat monitoring/cloudwatch-agent-config.json)
EOF

# Start agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
  -s

echo "✅ CloudWatch Agent started. Logs flowing to ${LOG_GROUP}."
