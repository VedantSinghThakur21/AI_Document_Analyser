# Monitoring & Security — Free-Tier Friendly

This guide adds CloudWatch-based monitoring with minimal cost and clear visibility into health, logs, and errors.

## What You Get
- CloudWatch Agent sending:
  - CPU, memory, disk, network metrics
  - Backend logs from `/home/ec2-user/backend/backend.log`
- Log group: `/doc-analyzer/backend` with 7-day retention
- Alarms (via SNS):
  - High CPU > 80% for 5 minutes
  - Low disk space (used > 90%)
  - Backend error spikes (ERROR lines in logs)

## 1) IAM Permissions
Ensure your EC2 instance role includes permissions for:
- `CloudWatchAgentServerPolicy`
- `AmazonSSMManagedInstanceCore` (optional but useful)
- CloudWatch Logs/PutLogEvents (included in the agent policy)

Attach managed policy:
```bash
aws iam attach-role-policy \
  --role-name EC2-DocumentAnalyzer-S3-Role \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
```

## 2) Deploy CloudWatch Agent
```bash
# Copy files to EC2
scp -i "your-key.pem" monitoring/cloudwatch-agent-config.json ec2-user@<EC2_PUBLIC_IP>:/home/ec2-user/
scp -i "your-key.pem" monitoring/deploy_cloudwatch_monitoring.sh ec2-user@<EC2_PUBLIC_IP>:/home/ec2-user/

# SSH and run
ssh -i "your-key.pem" ec2-user@<EC2_PUBLIC_IP>
bash deploy_cloudwatch_monitoring.sh ap-south-1
```

## 3) Create Alarms (SNS)
```bash
# On EC2 (or local with role/creds)
bash monitoring/create_alarms.sh ap-south-1 doc-analyzer-alerts

# Then subscribe your email (one-time)
aws sns subscribe --topic-arn arn:aws:sns:<REGION>:<ACCOUNT_ID>:doc-analyzer-alerts \
  --protocol email --notification-endpoint you@example.com --region ap-south-1
```

## 4) Verify
- Metrics: CloudWatch > Metrics > CWAgent and AWS/EC2
- Logs: CloudWatch > Logs > Log groups > `/doc-analyzer/backend`
- Alarms: CloudWatch > Alarms

## Cost Notes (Free Tier)
- CloudWatch free tier includes 5GB logs ingest, 5GB archive, 3 dashboards, 10 metrics, 10 alarms (varies). Our setup is conservative.
- 7-day retention prevents unnecessary storage.
- SNS emails are free.

## Optional Hardening
- Tighten security group to your IP
- Set S3 Block Public Access
- Add bucket policy to require TLS
- Lock CORS to your GitHub Pages origin

## Rollback
To stop the agent:
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a stop
```
To delete alarms and topic:
```bash
aws cloudwatch delete-alarms --alarm-names DocAnalyzer-HighCPU DocAnalyzer-LowDisk DocAnalyzer-BackendErrors --region ap-south-1
aws sns delete-topic --topic-arn arn:aws:sns:<REGION>:<ACCOUNT_ID>:doc-analyzer-alerts
```