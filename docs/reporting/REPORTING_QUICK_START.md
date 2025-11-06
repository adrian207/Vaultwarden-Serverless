# Reporting Quick Start Guide

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Estimated Time:** 2-4 hours  
**Difficulty:** Medium

## Get Security Dashboards Running in 2 Hours

This guide walks you through setting up essential security monitoring and reporting for your Vaultwarden deployment.

---

## What You'll Build

By the end of this guide:
- ✅ Real-time monitoring dashboard
- ✅ Automated security alerts
- ✅ Failed login detection
- ✅ Usage analytics
- ✅ Daily security summary email

**Cost:** $10-50/month (cloud-native monitoring)

---

## Prerequisites

- ✅ Vaultwarden deployed on AWS or GCP
- ✅ Admin access to cloud console
- ✅ API access to Vaultwarden (for event export)

---

## Option A: AWS CloudWatch (60 minutes)

### Step 1: Enable Container Insights (10 minutes)

```bash
# Enable Container Insights for ECS
aws ecs update-cluster-settings \
  --cluster vaultwarden-cluster \
  --settings name=containerInsights,value=enabled \
  --region us-east-1

# Verify
aws ecs describe-clusters \
  --clusters vaultwarden-cluster \
  --region us-east-1 \
  --query 'clusters[0].settings'
```

✅ **Container Insights enabled!**

---

### Step 2: Create Monitoring Dashboard (20 minutes)

1. **Navigate to CloudWatch**
   - AWS Console → CloudWatch → Dashboards

2. **Create Dashboard**
   - Click "Create dashboard"
   - Name: `vaultwarden-monitoring`
   - Click "Create dashboard"

3. **Add Widgets**

**Widget 1: Service Health**
```json
{
  "metrics": [
    ["AWS/ApplicationELB", "TargetResponseTime", {"stat": "Average"}],
    [".", "HTTPCode_Target_2XX_Count", {"stat": "Sum"}],
    [".", "HTTPCode_Target_5XX_Count", {"stat": "Sum"}]
  ],
  "period": 300,
  "stat": "Average",
  "region": "us-east-1",
  "title": "Service Health"
}
```

**Widget 2: ECS Performance**
```json
{
  "metrics": [
    ["AWS/ECS", "CPUUtilization", {"stat": "Average"}],
    [".", "MemoryUtilization", {"stat": "Average"}]
  ],
  "period": 300,
  "stat": "Average",
  "region": "us-east-1",
  "title": "ECS Performance"
}
```

**Widget 3: Database**
```json
{
  "metrics": [
    ["AWS/RDS", "DatabaseConnections", {"stat": "Average"}],
    [".", "CPUUtilization", {"stat": "Average"}],
    [".", "FreeableMemory", {"stat": "Average"}]
  ],
  "period": 300,
  "stat": "Average",
  "region": "us-east-1",
  "title": "Database Performance"
}
```

✅ **Dashboard created!**

---

### Step 3: Set Up Alerts (15 minutes)

**Alert 1: High Error Rate**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name vaultwarden-high-error-rate \
  --alarm-description "Alert when error rate is high" \
  --metric-name HTTPCode_Target_5XX_Count \
  --namespace AWS/ApplicationELB \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:vaultwarden-alerts
```

**Alert 2: Service Down**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name vaultwarden-service-down \
  --alarm-description "Alert when service is unreachable" \
  --metric-name HealthyHostCount \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 60 \
  --evaluation-periods 2 \
  --threshold 1 \
  --comparison-operator LessThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:vaultwarden-alerts
```

**Alert 3: High CPU**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name vaultwarden-high-cpu \
  --alarm-description "Alert when CPU is high" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:vaultwarden-alerts
```

✅ **Alerts configured!**

---

### Step 4: Export Event Logs (15 minutes)

**Create Lambda Function:**

```python
import json
import boto3
import requests
from datetime import datetime, timedelta

s3 = boto3.client('s3')

VAULT_URL = "https://vault.yourcompany.com"
API_TOKEN = "your-api-token"
ORG_ID = "your-org-id"
S3_BUCKET = "vaultwarden-events"

def lambda_handler(event, context):
    """Export Vaultwarden events to S3"""
    
    # Fetch yesterday's events
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    url = f"{VAULT_URL}/api/organizations/{ORG_ID}/events"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {
        "start": start_date.isoformat(),
        "end": end_date.isoformat()
    }
    
    response = requests.get(url, headers=headers, params=params)
    events = response.json()['data']
    
    # Save to S3
    key = f"events/{start_date.strftime('%Y/%m/%d')}/events.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(events),
        ContentType='application/json'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Exported {len(events)} events')
    }
```

**Deploy Lambda:**

```bash
# Create deployment package
zip -r function.zip lambda_function.py

# Create function
aws lambda create-function \
  --function-name export-vaultwarden-events \
  --runtime python3.9 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip

# Schedule daily execution
aws events put-rule \
  --name export-vaultwarden-events-daily \
  --schedule-expression "cron(0 2 * * ? *)"

aws events put-targets \
  --rule export-vaultwarden-events-daily \
  --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:ACCOUNT:function:export-vaultwarden-events"
```

✅ **Event export automated!**

---

## Option B: GCP Cloud Monitoring (60 minutes)

### Step 1: Enable Monitoring (5 minutes)

```bash
# Enable APIs
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com

# Verify
gcloud services list --enabled | grep monitoring
```

✅ **Monitoring enabled!**

---

### Step 2: Create Dashboard (20 minutes)

**Create dashboard.json:**

```json
{
  "displayName": "Vaultwarden Monitoring",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Cloud Run Requests",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "xPos": 6,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Cloud Run Latency",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_latencies\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_DELTA",
                    "crossSeriesReducer": "REDUCE_PERCENTILE_95"
                  }
                }
              }
            }]
          }
        }
      }
    ]
  }
}
```

**Deploy dashboard:**

```bash
gcloud monitoring dashboards create --config-from-file=dashboard.json
```

✅ **Dashboard created!**

---

### Step 3: Create Alerts (15 minutes)

**Alert Policy 1: High Error Rate**

```yaml
# alert-policy-errors.yaml
displayName: "Vaultwarden High Error Rate"
conditions:
  - displayName: "Error rate > 5%"
    conditionThreshold:
      filter: 'resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_count" AND metric.label.response_code_class="5xx"'
      comparison: COMPARISON_GT
      thresholdValue: 5
      duration: 300s
      aggregations:
        - alignmentPeriod: 60s
          perSeriesAligner: ALIGN_RATE
notificationChannels:
  - projects/PROJECT_ID/notificationChannels/CHANNEL_ID
```

```bash
gcloud alpha monitoring policies create --policy-from-file=alert-policy-errors.yaml
```

**Alert Policy 2: High Latency**

```yaml
# alert-policy-latency.yaml
displayName: "Vaultwarden High Latency"
conditions:
  - displayName: "P95 latency > 1000ms"
    conditionThreshold:
      filter: 'resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_latencies"'
      comparison: COMPARISON_GT
      thresholdValue: 1000
      duration: 300s
      aggregations:
        - alignmentPeriod: 60s
          perSeriesAligner: ALIGN_DELTA
          crossSeriesReducer: REDUCE_PERCENTILE_95
notificationChannels:
  - projects/PROJECT_ID/notificationChannels/CHANNEL_ID
```

```bash
gcloud alpha monitoring policies create --policy-from-file=alert-policy-latency.yaml
```

✅ **Alerts configured!**

---

### Step 4: Export Events (20 minutes)

**Create Cloud Function:**

```python
import functions_framework
import requests
import json
from datetime import datetime, timedelta
from google.cloud import storage

VAULT_URL = "https://vault.yourcompany.com"
API_TOKEN = "your-api-token"
ORG_ID = "your-org-id"
BUCKET_NAME = "vaultwarden-events"

@functions_framework.http
def export_events(request):
    """Export Vaultwarden events to Cloud Storage"""
    
    # Fetch yesterday's events
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    url = f"{VAULT_URL}/api/organizations/{ORG_ID}/events"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {
        "start": start_date.isoformat(),
        "end": end_date.isoformat()
    }
    
    response = requests.get(url, headers=headers, params=params)
    events = response.json()['data']
    
    # Save to Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"events/{start_date.strftime('%Y/%m/%d')}/events.json")
    blob.upload_from_string(json.dumps(events), content_type='application/json')
    
    return {
        'status': 'success',
        'events_exported': len(events)
    }
```

**Deploy Function:**

```bash
gcloud functions deploy export-vaultwarden-events \
  --runtime python39 \
  --trigger-http \
  --entry-point export_events \
  --region us-central1

# Schedule daily execution
gcloud scheduler jobs create http export-vaultwarden-events \
  --schedule="0 2 * * *" \
  --uri="https://us-central1-PROJECT.cloudfunctions.net/export-vaultwarden-events" \
  --http-method=GET
```

✅ **Event export automated!**

---

## Step 5: Query Event Logs (30 minutes)

### Create BigQuery Dataset (AWS: Athena / Redshift Serverless)

**GCP:**

```bash
# Create dataset
bq mk --dataset --location=US vaultwarden_analytics

# Create table
bq mk --table \
  vaultwarden_analytics.events \
  event_id:STRING,timestamp:TIMESTAMP,user_email:STRING,event_type:STRING,ip_address:STRING,details:STRING
```

**Load data from Cloud Storage:**

```bash
bq load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --autodetect \
  vaultwarden_analytics.events \
  gs://vaultwarden-events/events/*/*/*.json
```

---

### Useful Queries

**Failed Login Attempts (Last 7 Days):**

```sql
SELECT 
  user_email,
  COUNT(*) as failed_attempts,
  ARRAY_AGG(DISTINCT ip_address) as ip_addresses,
  MAX(timestamp) as last_attempt
FROM `project.vaultwarden_analytics.events`
WHERE 
  event_type = 'login_failed'
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY user_email
HAVING failed_attempts > 3
ORDER BY failed_attempts DESC;
```

**Daily Active Users:**

```sql
SELECT 
  DATE(timestamp) as date,
  COUNT(DISTINCT user_email) as dau
FROM `project.vaultwarden_analytics.events`
WHERE 
  event_type IN ('login', 'item_viewed')
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date;
```

**Most Accessed Items:**

```sql
SELECT 
  JSON_EXTRACT_SCALAR(details, '$.item_name') as item_name,
  COUNT(*) as access_count,
  COUNT(DISTINCT user_email) as unique_users
FROM `project.vaultwarden_analytics.events`
WHERE 
  event_type = 'item_viewed'
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY item_name
ORDER BY access_count DESC
LIMIT 20;
```

✅ **Queries ready!**

---

## Step 6: Automated Daily Report (30 minutes)

**Create Python Script:**

```python
#!/usr/bin/env python3
"""
Daily Security Summary Email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import bigquery
from datetime import datetime, timedelta

client = bigquery.Client()

def get_failed_logins():
    """Get failed login attempts from yesterday"""
    query = """
    SELECT 
      user_email,
      COUNT(*) as attempts,
      ARRAY_AGG(DISTINCT ip_address) as ips
    FROM `project.vaultwarden_analytics.events`
    WHERE 
      event_type = 'login_failed'
      AND DATE(timestamp) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    GROUP BY user_email
    ORDER BY attempts DESC
    """
    return client.query(query).to_dataframe()

def get_new_users():
    """Get new user signups from yesterday"""
    query = """
    SELECT 
      user_email,
      timestamp
    FROM `project.vaultwarden_analytics.events`
    WHERE 
      event_type = 'user_confirmed'
      AND DATE(timestamp) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    ORDER BY timestamp DESC
    """
    return client.query(query).to_dataframe()

def send_email(subject, html):
    """Send email via SMTP"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'vaultwarden@company.com'
    msg['To'] = 'security@company.com'
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your-email@company.com', 'app-password')
        server.send_message(msg)

def generate_report():
    """Generate and send daily security report"""
    
    failed_logins = get_failed_logins()
    new_users = get_new_users()
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
    <h1>Vaultwarden Daily Security Summary</h1>
    <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
    
    <h2>Failed Login Attempts: {len(failed_logins)}</h2>
    {failed_logins.to_html(index=False) if len(failed_logins) > 0 else '<p>No failed logins yesterday ✅</p>'}
    
    <h2>New Users: {len(new_users)}</h2>
    {new_users.to_html(index=False) if len(new_users) > 0 else '<p>No new users yesterday</p>'}
    
    <hr>
    <p style="color: #666; font-size: 12px;">
    This is an automated report from Vaultwarden.<br>
    Dashboard: https://console.cloud.google.com/monitoring/dashboards
    </p>
    </body>
    </html>
    """
    
    send_email(
        subject=f"Vaultwarden Daily Security Summary - {datetime.now().strftime('%Y-%m-%d')}",
        html=html
    )

if __name__ == "__main__":
    generate_report()
```

**Schedule with Cloud Scheduler:**

```bash
gcloud scheduler jobs create http daily-security-report \
  --schedule="0 8 * * *" \
  --uri="https://your-cloud-function-url" \
  --http-method=POST
```

✅ **Daily report automated!**

---

## Success Checklist

- [ ] Cloud monitoring enabled
- [ ] Dashboard created with key metrics
- [ ] Alerts configured (errors, latency, service down)
- [ ] Event logs exported to storage
- [ ] Event analytics queries working
- [ ] Daily security report automated
- [ ] Test alerts triggered successfully
- [ ] Team trained on dashboard access

**All checked?** ✅ You're monitoring production!

---

## What's Next?

### Short Term (This Week)

1. **Refine alerts**
   - Adjust thresholds based on actual patterns
   - Add more alert conditions as needed

2. **Add more queries**
   - Security-specific queries
   - Usage analytics
   - Compliance reports

3. **Share dashboard**
   - Give team members read access
   - Document how to use dashboard

### Medium Term (This Month)

4. **Advanced dashboards**
   - Executive summary dashboard
   - DevOps monitoring dashboard
   - Compliance dashboard

5. **Weekly reports**
   - Usage trends
   - Security summary
   - Performance metrics

### Long Term (Ongoing)

6. **Continuous improvement**
   - Add new metrics as needed
   - Refine alert conditions
   - Automate more reports

7. **Integration**
   - SIEM integration (Splunk, Sentinel)
   - BI tools (Tableau, Power BI)
   - Incident response tools

---

## Cost Summary

**AWS:**
- CloudWatch: $10-30/month
- S3 storage: $1-5/month
- Lambda: $0-5/month
- **Total: $11-40/month**

**GCP:**
- Cloud Monitoring: $8-25/month
- Cloud Storage: $1-5/month
- Cloud Functions: $0-5/month
- BigQuery: $5-20/month
- **Total: $14-55/month**

**vs Commercial Solutions:**
- Splunk: $150-500/month
- Datadog: $100-300/month
- **Savings: 80-90%**

---

## Troubleshooting

### Issue: No metrics showing in dashboard

**Solutions:**
1. Wait 5-10 minutes for initial data collection
2. Verify Container Insights / Cloud Monitoring enabled
3. Check metric names and namespaces are correct
4. Verify service is receiving traffic

---

### Issue: Alerts not firing

**Solutions:**
1. Manually trigger condition (e.g., stop service)
2. Verify SNS topic / notification channel configured
3. Check email/SMS settings
4. Review alert policy thresholds

---

### Issue: Event export failing

**Solutions:**
1. Verify API token has correct permissions
2. Check organization ID is correct
3. Verify network connectivity from Lambda/Function
4. Review function logs for errors

---

## Support & Resources

### Documentation
- 📋 **[Complete Reporting Guide](REPORTING_ANALYTICS_GUIDE.md)** - Full documentation
- 📈 **[Monitoring Guide](../operations/MONITORING.md)** - Infrastructure monitoring
- 🔒 **[Security Guide](../operations/SECURITY.md)** - Security best practices

### Cloud Provider Docs
- **AWS CloudWatch:** [docs.aws.amazon.com/cloudwatch](https://docs.aws.amazon.com/cloudwatch/)
- **GCP Cloud Monitoring:** [cloud.google.com/monitoring/docs](https://cloud.google.com/monitoring/docs)

### Need Help?
- **Email:** adrian207@gmail.com
- **Documentation:** Review complete guide above

---

## Conclusion

**You now have production monitoring and security analytics!**

**What you've accomplished:**
- ✅ Real-time monitoring dashboard
- ✅ Automated security alerts
- ✅ Event log analytics
- ✅ Daily security reports
- ✅ Cost-effective solution ($15-55/month)

**Total setup time:** 2-4 hours

**Next:** Refine alerts, add more analytics, integrate with existing tools

---

**Setup Time:** 2-4 hours  
**Monthly Cost:** $15-55  
**Value:** Enterprise-grade monitoring and analytics

**Questions?** adrian207@gmail.com

**Last Updated:** November 5, 2025

