#!/bin/bash
set -e
REGION=${1:-ap-south-1}
SNS_TOPIC_NAME=${2:-doc-analyzer-alerts}

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create SNS topic
TOPIC_ARN=$(aws sns create-topic --name ${SNS_TOPIC_NAME} --query TopicArn --output text --region ${REGION})
echo "SNS Topic: ${TOPIC_ARN}"

echo "Subscribe your email to SNS (one-time):"
echo "aws sns subscribe --topic-arn ${TOPIC_ARN} --protocol email --notification-endpoint you@example.com --region ${REGION}"

# Alarm 1: High CPU (>80% for 5 minutes)
aws cloudwatch put-metric-alarm \
  --alarm-name "DocAnalyzer-HighCPU" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 60 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=$(curl -s http://169.254.169.254/latest/meta-data/instance-id) \
  --evaluation-periods 5 \
  --alarm-actions ${TOPIC_ARN} \
  --ok-actions ${TOPIC_ARN} \
  --region ${REGION}

# Alarm 2: Low disk space (<10% free)
aws cloudwatch put-metric-alarm \
  --alarm-name "DocAnalyzer-LowDisk" \
  --metric-name disk_used_percent \
  --namespace CWAgent \
  --statistic Average \
  --period 60 \
  --threshold 90 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=$(curl -s http://169.254.169.254/latest/meta-data/instance-id),Name=path,Value=/,Name=ImageId,Value=*,Name=device,Value=*,Name=fstype,Value=* \
  --evaluation-periods 5 \
  --alarm-actions ${TOPIC_ARN} \
  --ok-actions ${TOPIC_ARN} \
  --region ${REGION}

# Alarm 3: Backend log error rate (using Metric Filter)
LOG_GROUP="/doc-analyzer/backend"

# Create metric filter for "ERROR" lines
aws logs put-metric-filter \
  --log-group-name ${LOG_GROUP} \
  --filter-name BackendErrorFilter \
  --filter-pattern "ERROR" \
  --metric-transformations metricName=BackendErrorCount,metricNamespace=DocAnalyzer,metricValue=1 --region ${REGION}

# Alarm when errors > 5 in 5 minutes
aws cloudwatch put-metric-alarm \
  --alarm-name "DocAnalyzer-BackendErrors" \
  --metric-name BackendErrorCount \
  --namespace DocAnalyzer \
  --statistic Sum \
  --period 60 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 5 \
  --alarm-actions ${TOPIC_ARN} \
  --ok-actions ${TOPIC_ARN} \
  --region ${REGION}

echo "✅ Alarms created. Remember to confirm the email subscription for SNS notifications."