# Advanced Reporting & Analytics Guide

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Date:** November 5, 2025  
**Status:** Documentation Complete - Ready for Implementation

## Executive Summary

Transform your Vaultwarden deployment from basic password management into a data-driven security platform with comprehensive reporting and analytics.

**What You'll Get:**
- ✅ Real-time security dashboards
- ✅ User activity analytics
- ✅ Compliance reporting
- ✅ Security incident detection
- ✅ Usage metrics and trends
- ✅ Automated alerting
- ✅ Executive summaries
- ✅ Custom reports

**Cost:** $10-200/month (depending on scale and tools)

**Implementation Time:** 1-4 weeks (depending on complexity)

---

## Available Data Sources

### 1. Vaultwarden Event Logs

**What's Logged:**
- User login events
- Failed login attempts
- Item creation/modification/deletion
- Item access (views)
- Collection access
- User invitations
- Permission changes
- Organization changes
- Two-factor authentication events
- Emergency access requests

**Access Methods:**
- Web UI: Organization → Manage → Events
- API: `/api/organizations/{orgId}/events`
- Database: Direct queries (advanced)

**Retention:** Configurable (default: unlimited in self-hosted)

---

### 2. Application Logs

**What's Logged:**
- HTTP requests
- Application errors
- Performance metrics
- Database queries (if enabled)
- Authentication attempts
- Rate limiting events

**Location:**
- Container stdout/stderr
- Cloud logging (CloudWatch, Cloud Logging, Application Insights)

**Format:** JSON (structured) or text

---

### 3. Infrastructure Metrics

**What's Available:**
- CPU utilization
- Memory usage
- Request count
- Request latency
- Database connections
- Database performance
- Storage usage
- Network traffic

**Source:** Cloud provider monitoring
- AWS: CloudWatch
- GCP: Cloud Monitoring
- Azure: Azure Monitor

---

### 4. Database Audit Logs

**What's Logged:**
- Database connections
- Query execution
- Slow queries
- Failed queries
- User changes

**Access:** Database-specific logging
- Aurora: CloudWatch Logs
- Cloud SQL: Cloud Logging
- Cosmos DB: Diagnostic logs

---

## Reporting Architecture Options

### Option 1: Cloud-Native Monitoring ⭐ **RECOMMENDED**

**Components:**
- AWS CloudWatch / GCP Cloud Monitoring / Azure Monitor (metrics)
- Built-in dashboards
- Log analytics
- Automated alerting

**Pros:**
- ✅ No additional infrastructure
- ✅ Integrated with deployment
- ✅ Automatic data collection
- ✅ Low cost ($10-50/month)
- ✅ Quick setup (1-2 days)

**Cons:**
- ❌ Limited customization
- ❌ Cloud provider lock-in
- ❌ Basic visualizations

**Best For:** Small to medium deployments (< 1,000 users), quick implementation

**Cost:** $10-50/month

---

### Option 2: ELK Stack (Elasticsearch, Logstash, Kibana)

**Components:**
- Elasticsearch (data storage & search)
- Logstash or Fluentd (log collection)
- Kibana (visualization)

**Pros:**
- ✅ Powerful search capabilities
- ✅ Rich visualizations
- ✅ Flexible data processing
- ✅ Open source

**Cons:**
- ❌ Complex setup
- ❌ High resource requirements
- ❌ Ongoing maintenance
- ❌ Higher cost ($100-500/month)

**Best For:** Large deployments (> 1,000 users), advanced analytics needs

**Cost:** $100-500/month (managed) or infrastructure costs (self-hosted)

---

### Option 3: Grafana + Prometheus

**Components:**
- Prometheus (metrics collection & storage)
- Grafana (visualization)
- Loki (log aggregation, optional)

**Pros:**
- ✅ Beautiful dashboards
- ✅ Powerful alerting
- ✅ Open source
- ✅ Active community

**Cons:**
- ❌ Requires metrics instrumentation
- ❌ Additional infrastructure
- ❌ Maintenance overhead

**Best For:** DevOps-focused teams, custom metrics needs

**Cost:** $50-200/month (managed) or infrastructure costs

---

### Option 4: Commercial BI Tools

**Options:**
- Tableau
- Power BI
- Looker
- Metabase

**Approach:**
- Export Vaultwarden data to data warehouse
- Connect BI tool to data warehouse
- Create custom reports and dashboards

**Pros:**
- ✅ Professional reports
- ✅ Executive-friendly
- ✅ Advanced analytics
- ✅ Customizable

**Cons:**
- ❌ Expensive ($15-70/user/month)
- ❌ Complex data pipeline
- ❌ Requires data engineering

**Best For:** Enterprises with existing BI infrastructure, executive reporting needs

**Cost:** $150-700/month (10 users) + data warehouse costs

---

## Recommended Implementation

### Phase 1: Cloud-Native Monitoring (Week 1)

**Quick wins with minimal effort:**

#### AWS CloudWatch Setup

1. **Enable Container Insights**
   ```bash
   aws ecs update-cluster-settings \
     --cluster vaultwarden-cluster \
     --settings name=containerInsights,value=enabled
   ```

2. **Create Custom Dashboard**
   - CloudWatch → Dashboards → Create dashboard
   - Add widgets:
     - ECS CPU/Memory utilization
     - Request count
     - Error rate
     - Database connections
     - Response time

3. **Set Up Alarms**
   ```bash
   # High error rate alarm
   aws cloudwatch put-metric-alarm \
     --alarm-name vaultwarden-high-error-rate \
     --comparison-operator GreaterThanThreshold \
     --evaluation-periods 2 \
     --metric-name 5XXError \
     --namespace AWS/ApplicationELB \
     --period 300 \
     --statistic Sum \
     --threshold 10 \
     --alarm-actions arn:aws:sns:region:account:alerts
   ```

---

#### GCP Cloud Monitoring Setup

1. **Enable Monitoring**
   ```bash
   gcloud services enable monitoring.googleapis.com
   ```

2. **Create Dashboard**
   - Cloud Monitoring → Dashboards → Create Dashboard
   - Add charts:
     - Cloud Run request count
     - Cloud Run latency
     - Cloud SQL connections
     - Error rate

3. **Create Alert Policies**
   ```bash
   gcloud alpha monitoring policies create \
     --notification-channels=CHANNEL_ID \
     --display-name="Vaultwarden High Error Rate" \
     --condition-display-name="Error rate > 5%" \
     --condition-threshold-value=5 \
     --condition-threshold-duration=300s
   ```

---

### Phase 2: Event Log Analytics (Week 2)

#### Export Events to Data Store

**Option A: Scheduled Export Script**

```python
#!/usr/bin/env python3
"""
Export Vaultwarden events to data warehouse
"""

import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from google.cloud import bigquery  # or boto3 for Redshift

VAULT_URL = "https://vault.yourcompany.com"
API_TOKEN = "your-api-token"
ORG_ID = "your-org-id"

def fetch_events(start_date, end_date):
    """Fetch events from Vaultwarden API"""
    url = f"{VAULT_URL}/api/organizations/{ORG_ID}/events"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {
        "start": start_date.isoformat(),
        "end": end_date.isoformat()
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['data']

def load_to_bigquery(events):
    """Load events to BigQuery"""
    client = bigquery.Client()
    table_id = "project.dataset.vaultwarden_events"
    
    # Transform events
    df = pd.DataFrame(events)
    df['timestamp'] = pd.to_datetime(df['date'])
    
    # Load to BigQuery
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    
    print(f"Loaded {len(events)} events to BigQuery")

if __name__ == "__main__":
    # Fetch yesterday's events
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    events = fetch_events(start_date, end_date)
    load_to_bigquery(events)
```

**Schedule with Cloud Scheduler:**
```bash
# GCP
gcloud scheduler jobs create http export-vaultwarden-events \
  --schedule="0 2 * * *" \
  --uri="https://your-function-url" \
  --http-method=POST

# AWS (use EventBridge + Lambda)
aws events put-rule \
  --name export-vaultwarden-events \
  --schedule-expression "cron(0 2 * * ? *)"
```

---

**Option B: Real-Time Streaming**

```python
"""
Stream Vaultwarden events in real-time
"""

import asyncio
import websockets
import json
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project', 'vaultwarden-events')

async def stream_events():
    """Stream events from Vaultwarden"""
    # Implementation depends on Vaultwarden's capabilities
    # May need to poll API regularly
    
    while True:
        events = fetch_new_events()
        
        for event in events:
            # Publish to Pub/Sub (GCP) or SNS (AWS)
            data = json.dumps(event).encode('utf-8')
            publisher.publish(topic_path, data)
        
        await asyncio.sleep(60)  # Poll every minute

if __name__ == "__main__":
    asyncio.run(stream_events())
```

---

### Phase 3: Custom Dashboards (Week 3)

#### Security Dashboard

**Metrics to Track:**

1. **Authentication**
   - Successful logins (by user, by hour)
   - Failed login attempts
   - Failed login attempts by IP
   - 2FA bypass attempts
   - Average login time

2. **Access Patterns**
   - Most accessed items
   - Unusual access times (off-hours)
   - Geographic anomalies
   - New device logins

3. **Item Activity**
   - Items created/modified/deleted
   - Password changes
   - Shared items
   - Items never accessed (stale)

4. **Security Health**
   - Users without 2FA
   - Weak master passwords
   - Password reuse
   - Exposed passwords (breach database)

**Example SQL Queries (BigQuery):**

```sql
-- Failed login attempts by user (last 7 days)
SELECT 
  user_email,
  COUNT(*) as failed_attempts,
  MIN(timestamp) as first_attempt,
  MAX(timestamp) as last_attempt
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type = 'login_failed'
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY user_email
HAVING failed_attempts > 5
ORDER BY failed_attempts DESC;

-- Most accessed items
SELECT 
  item_name,
  COUNT(*) as access_count,
  COUNT(DISTINCT user_email) as unique_users
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type = 'item_viewed'
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY item_name
ORDER BY access_count DESC
LIMIT 20;

-- Off-hours access (outside 8 AM - 6 PM)
SELECT 
  user_email,
  item_name,
  timestamp,
  EXTRACT(HOUR FROM timestamp) as hour
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type = 'item_viewed'
  AND (EXTRACT(HOUR FROM timestamp) < 8 OR EXTRACT(HOUR FROM timestamp) > 18)
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY timestamp DESC;

-- Users without 2FA
SELECT 
  u.email,
  u.created_at,
  u.last_login
FROM users u
LEFT JOIN two_factor tf ON u.uuid = tf.user_uuid
WHERE tf.uuid IS NULL
ORDER BY u.last_login DESC;
```

---

#### Usage Analytics Dashboard

**Metrics to Track:**

1. **Adoption**
   - Active users (DAU, WAU, MAU)
   - New user signups
   - User growth rate
   - Feature adoption rates

2. **Engagement**
   - Logins per user
   - Items per user
   - Collections used
   - Organization participation

3. **Performance**
   - Average login time
   - API response times
   - Database query performance
   - Error rates

4. **Storage**
   - Total items stored
   - Items per organization
   - File attachment usage
   - Database size growth

**Example Queries:**

```sql
-- Daily Active Users (DAU)
SELECT 
  DATE(timestamp) as date,
  COUNT(DISTINCT user_email) as dau
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type IN ('login', 'item_viewed', 'item_created')
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date;

-- Feature adoption
SELECT 
  'Organizations' as feature,
  COUNT(DISTINCT user_uuid) as users_using,
  ROUND(COUNT(DISTINCT user_uuid) * 100.0 / (SELECT COUNT(*) FROM users), 2) as adoption_rate
FROM organization_users
UNION ALL
SELECT 
  '2FA' as feature,
  COUNT(DISTINCT user_uuid) as users_using,
  ROUND(COUNT(DISTINCT user_uuid) * 100.0 / (SELECT COUNT(*) FROM users), 2) as adoption_rate
FROM two_factor
UNION ALL
SELECT 
  'Send' as feature,
  COUNT(DISTINCT user_uuid) as users_using,
  ROUND(COUNT(DISTINCT user_uuid) * 100.0 / (SELECT COUNT(*) FROM users), 2) as adoption_rate
FROM sends;

-- Items per user distribution
SELECT 
  items_count,
  COUNT(*) as user_count
FROM (
  SELECT 
    user_uuid,
    COUNT(*) as items_count
  FROM ciphers
  GROUP BY user_uuid
) 
GROUP BY items_count
ORDER BY items_count;
```

---

### Phase 4: Compliance Reporting (Week 4)

#### SOC 2 / ISO 27001 Reports

**Required Reports:**

1. **Access Control**
   - User provisioning/deprovisioning logs
   - Permission changes
   - Role assignments
   - Failed access attempts

2. **Audit Trail**
   - All login events
   - All data access events
   - All configuration changes
   - Admin actions

3. **Security Monitoring**
   - Failed login attempts
   - Unusual access patterns
   - Security incidents
   - Response actions

4. **Data Protection**
   - Encryption status
   - Backup verification
   - Data retention compliance
   - Data deletion logs

**Example Report Queries:**

```sql
-- User access control changes (last quarter)
SELECT 
  timestamp,
  acting_user_email,
  target_user_email,
  event_type,
  details
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type IN (
    'user_invited',
    'user_confirmed',
    'user_removed',
    'role_changed',
    'collection_access_changed'
  )
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY timestamp DESC;

-- Failed authentication attempts (security monitoring)
SELECT 
  DATE(timestamp) as date,
  user_email,
  ip_address,
  COUNT(*) as failed_attempts
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type = 'login_failed'
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date, user_email, ip_address
HAVING failed_attempts >= 3
ORDER BY date DESC, failed_attempts DESC;

-- Admin actions audit
SELECT 
  timestamp,
  user_email,
  event_type,
  details,
  ip_address
FROM `project.dataset.vaultwarden_events`
WHERE 
  user_role IN ('Owner', 'Admin')
  AND event_type IN (
    'organization_updated',
    'policy_updated',
    'user_removed',
    'collection_deleted'
  )
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY timestamp DESC;
```

**Automated Report Generation:**

```python
#!/usr/bin/env python3
"""
Generate compliance reports
"""

from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def generate_quarterly_report():
    """Generate quarterly compliance report"""
    client = bigquery.Client()
    
    # Run queries
    access_control_changes = client.query(ACCESS_CONTROL_QUERY).to_dataframe()
    failed_auth_attempts = client.query(FAILED_AUTH_QUERY).to_dataframe()
    admin_actions = client.query(ADMIN_ACTIONS_QUERY).to_dataframe()
    
    # Generate Excel report
    with pd.ExcelWriter('compliance_report.xlsx') as writer:
        access_control_changes.to_excel(writer, sheet_name='Access Control', index=False)
        failed_auth_attempts.to_excel(writer, sheet_name='Failed Auth', index=False)
        admin_actions.to_excel(writer, sheet_name='Admin Actions', index=False)
    
    # Email report
    send_email_with_attachment(
        to='compliance@company.com',
        subject=f'Quarterly Compliance Report - {datetime.now().strftime("%Y Q%q")}',
        body='Please find attached the quarterly compliance report for Vaultwarden.',
        attachment='compliance_report.xlsx'
    )

# Schedule to run quarterly
if __name__ == "__main__":
    generate_quarterly_report()
```

---

## Pre-Built Dashboard Templates

### Template 1: Security Operations Dashboard

**Widgets:**

1. **Top Left: Authentication Overview**
   - Total logins today
   - Failed login attempts
   - New users this week
   - 2FA adoption rate

2. **Top Right: Recent Security Events**
   - Failed logins (last hour)
   - Unusual access patterns
   - New device logins
   - Emergency access requests

3. **Bottom Left: User Activity Heatmap**
   - Logins by hour/day
   - Geographic distribution
   - Peak usage times

4. **Bottom Right: Security Health Score**
   - Users with 2FA: 95% ✅
   - Weak passwords: 5 ⚠️
   - Exposed passwords: 2 ❌
   - Items never accessed: 15 ℹ️

---

### Template 2: Executive Summary Dashboard

**Widgets:**

1. **Active Users**
   - DAU: 250
   - WAU: 500
   - MAU: 750
   - Growth: +15% MoM

2. **Usage Metrics**
   - Total items: 10,500
   - Items per user: 14
   - Organizations: 5
   - Shared items: 2,300

3. **Security Posture**
   - 2FA enabled: 98%
   - Password health: 92/100
   - Failed logins: 0.5%
   - Incidents: 0

4. **Cost Savings**
   - vs 1Password: $45,000/year
   - vs LastPass: $36,000/year
   - Infrastructure: $300/month

---

### Template 3: DevOps Monitoring Dashboard

**Widgets:**

1. **Application Performance**
   - Response time (p50/p95/p99)
   - Request rate
   - Error rate
   - Availability (99.9%)

2. **Infrastructure Health**
   - CPU utilization
   - Memory usage
   - Database connections
   - Storage usage

3. **Database Performance**
   - Query latency
   - Slow queries
   - Connection pool
   - Replication lag

4. **Alerts & Incidents**
   - Open alerts: 0
   - Resolved today: 3
   - MTTR: 15 minutes
   - Uptime: 99.95%

---

## Automated Alerting

### Critical Alerts (Immediate Action)

**1. Multiple Failed Login Attempts**
```yaml
alert: HighFailedLoginRate
expr: rate(vaultwarden_failed_logins_total[5m]) > 5
for: 5m
labels:
  severity: critical
annotations:
  summary: "High failed login rate detected"
  description: "{{ $value }} failed logins per second in the last 5 minutes"
```

**2. Unusual Geographic Access**
```sql
-- Detect logins from unexpected countries
SELECT 
  user_email,
  country,
  COUNT(*) as login_count
FROM `project.dataset.vaultwarden_events`
WHERE 
  event_type = 'login'
  AND country NOT IN ('US', 'CA', 'UK')  -- Expected countries
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY user_email, country;
```

**3. Emergency Access Requested**
```
Alert when someone requests emergency access to another user's vault
```

**4. Service Down**
```yaml
alert: ServiceDown
expr: up{job="vaultwarden"} == 0
for: 1m
labels:
  severity: critical
annotations:
  summary: "Vaultwarden service is down"
```

---

### Warning Alerts (Review Within 24 Hours)

**1. High Error Rate**
```yaml
alert: HighErrorRate
expr: rate(vaultwarden_errors_total[5m]) > 0.05
for: 10m
labels:
  severity: warning
annotations:
  summary: "Error rate above 5%"
```

**2. Users Without 2FA**
```sql
-- Alert if >10% of active users don't have 2FA
SELECT 
  COUNT(*) as users_without_2fa,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM users), 2) as percentage
FROM users u
LEFT JOIN two_factor tf ON u.uuid = tf.user_uuid
WHERE tf.uuid IS NULL
  AND u.last_login >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
```

**3. Slow Database Queries**
```yaml
alert: SlowDatabaseQueries
expr: histogram_quantile(0.95, rate(database_query_duration_seconds_bucket[5m])) > 1
for: 10m
labels:
  severity: warning
annotations:
  summary: "95th percentile query latency above 1 second"
```

---

### Info Alerts (Monitoring Only)

**1. New User Signups**
```
Daily summary of new user registrations
```

**2. Large Data Export**
```
Alert when user exports >1000 items (potential data breach)
```

**3. Backup Completion**
```
Daily confirmation that automated backups completed successfully
```

---

## Report Automation

### Daily Reports

**Security Summary (emailed to security team):**
- Failed login attempts
- New user signups
- Password health changes
- Unusual access patterns

**Example Script:**

```python
#!/usr/bin/env python3
"""
Daily security summary email
"""

def generate_daily_summary():
    """Generate and email daily security summary"""
    
    # Gather data
    failed_logins = get_failed_logins_today()
    new_users = get_new_users_today()
    password_health_changes = get_password_health_changes()
    unusual_access = detect_unusual_access()
    
    # Generate HTML email
    html = f"""
    <html>
    <body>
    <h1>Vaultwarden Daily Security Summary</h1>
    <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
    
    <h2>Failed Login Attempts: {len(failed_logins)}</h2>
    {generate_failed_logins_table(failed_logins)}
    
    <h2>New Users: {len(new_users)}</h2>
    {generate_new_users_table(new_users)}
    
    <h2>Password Health Changes</h2>
    {generate_password_health_summary(password_health_changes)}
    
    <h2>Unusual Access Patterns: {len(unusual_access)}</h2>
    {generate_unusual_access_table(unusual_access)}
    
    </body>
    </html>
    """
    
    send_email(
        to='security@company.com',
        subject=f'Daily Security Summary - {datetime.now().strftime("%Y-%m-%d")}',
        html=html
    )

# Schedule with cron: 0 8 * * * (8 AM daily)
```

---

### Weekly Reports

**Executive Summary (emailed to leadership):**
- Active users (DAU/WAU/MAU)
- Feature adoption
- Security posture
- Incidents and resolutions

---

### Monthly Reports

**Compliance Report (for audit):**
- All access control changes
- All admin actions
- Security incidents
- Backup verification
- User access reviews

---

### Quarterly Reports

**Business Review:**
- User growth trends
- Cost savings analysis
- Security improvements
- Feature utilization
- ROI metrics

---

## Integration with SIEM Tools

### Splunk Integration

```python
"""
Send Vaultwarden events to Splunk HTTP Event Collector
"""

import requests
import json

SPLUNK_HEC_URL = "https://splunk.company.com:8088/services/collector"
SPLUNK_TOKEN = "your-hec-token"

def send_to_splunk(event):
    """Send event to Splunk"""
    payload = {
        "event": event,
        "sourcetype": "vaultwarden:events",
        "source": "vaultwarden",
        "index": "security"
    }
    
    headers = {
        "Authorization": f"Splunk {SPLUNK_TOKEN}"
    }
    
    response = requests.post(
        SPLUNK_HEC_URL,
        headers=headers,
        data=json.dumps(payload),
        verify=True
    )
    
    return response.status_code == 200
```

---

### Azure Sentinel Integration

```python
"""
Send Vaultwarden events to Azure Sentinel
"""

from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = LogsIngestionClient(
    endpoint="https://your-dce.ingest.monitor.azure.com",
    credential=credential
)

def send_to_sentinel(events):
    """Send events to Azure Sentinel"""
    client.upload(
        rule_id="dcr-xxxxx",
        stream_name="Custom-VaultwardenEvents_CL",
        logs=events
    )
```

---

### AWS Security Hub Integration

```python
"""
Send security findings to AWS Security Hub
"""

import boto3

securityhub = boto3.client('securityhub')

def send_finding(event):
    """Send finding to Security Hub"""
    finding = {
        'SchemaVersion': '2018-10-08',
        'Id': f"vaultwarden-{event['id']}",
        'ProductArn': f"arn:aws:securityhub:{region}:{account}:product/{account}/vaultwarden",
        'GeneratorId': 'vaultwarden-events',
        'AwsAccountId': account,
        'Types': ['Software and Configuration Checks/Vulnerabilities/CVE'],
        'CreatedAt': event['timestamp'],
        'UpdatedAt': event['timestamp'],
        'Severity': {
            'Label': determine_severity(event)
        },
        'Title': event['event_type'],
        'Description': event['details'],
        'Resources': [{
            'Type': 'Other',
            'Id': f"vaultwarden-instance-{instance_id}"
        }]
    }
    
    securityhub.batch_import_findings(Findings=[finding])
```

---

## Custom Metrics & KPIs

### Security KPIs

1. **Authentication Security Score**
   ```
   Score = (users_with_2fa / total_users) * 100
   Target: > 95%
   ```

2. **Password Health Score**
   ```
   Score = 100 - (weak_passwords + reused_passwords + exposed_passwords) / total_passwords * 100
   Target: > 90
   ```

3. **Access Anomaly Rate**
   ```
   Rate = unusual_access_events / total_access_events * 100
   Target: < 1%
   ```

4. **Mean Time to Detect (MTTD)**
   ```
   MTTD = avg(detection_time - incident_time)
   Target: < 5 minutes
   ```

5. **Mean Time to Respond (MTTR)**
   ```
   MTTR = avg(resolution_time - detection_time)
   Target: < 30 minutes
   ```

---

### Operational KPIs

1. **Service Availability**
   ```
   Availability = (total_uptime / total_time) * 100
   Target: > 99.9%
   ```

2. **Average Response Time**
   ```
   Avg Response Time = p95(request_duration)
   Target: < 500ms
   ```

3. **Error Rate**
   ```
   Error Rate = (errors / total_requests) * 100
   Target: < 0.1%
   ```

4. **Database Performance**
   ```
   Avg Query Time = p95(query_duration)
   Target: < 100ms
   ```

---

### Business KPIs

1. **User Adoption Rate**
   ```
   Adoption = (active_users / invited_users) * 100
   Target: > 80%
   ```

2. **Feature Utilization**
   ```
   Organization Usage = (users_in_orgs / total_users) * 100
   2FA Adoption = (users_with_2fa / total_users) * 100
   ```

3. **Cost Per User**
   ```
   Cost Per User = total_monthly_cost / active_users
   Benchmark: < $0.50/user (vs $5-7 commercial)
   ```

4. **ROI**
   ```
   Annual Savings = (commercial_cost - self_hosted_cost)
   ROI = (savings / implementation_cost) * 100
   ```

---

## Implementation Checklist

### Week 1: Foundation
- [ ] Enable cloud monitoring (CloudWatch / Cloud Monitoring)
- [ ] Create basic dashboard (CPU, memory, requests)
- [ ] Set up basic alerting (service down, high error rate)
- [ ] Document data sources
- [ ] Test alert delivery

### Week 2: Event Analytics
- [ ] Set up event log export
- [ ] Create data warehouse or analytics database
- [ ] Build initial queries (failed logins, user activity)
- [ ] Create event-based alerts
- [ ] Test end-to-end data pipeline

### Week 3: Dashboards
- [ ] Design security operations dashboard
- [ ] Design executive summary dashboard
- [ ] Build visualizations
- [ ] Share with stakeholders for feedback
- [ ] Refine based on feedback

### Week 4: Automation
- [ ] Set up automated daily reports
- [ ] Configure weekly summaries
- [ ] Create monthly compliance reports
- [ ] Document all reports and recipients
- [ ] Train team on using dashboards

---

## Cost Breakdown

### Small Deployment (< 100 users)

**Cloud-Native Only:**
- CloudWatch / Cloud Monitoring: $10-20/month
- Log storage: $5-10/month
- Alerting: Included
- **Total: $15-30/month**

---

### Medium Deployment (100-1,000 users)

**Cloud-Native + Data Warehouse:**
- CloudWatch / Cloud Monitoring: $30-50/month
- BigQuery / Redshift Serverless: $50-100/month
- Log storage: $20-30/month
- Alerting: Included
- **Total: $100-180/month**

---

### Large Deployment (1,000-10,000+ users)

**Full Analytics Stack:**
- CloudWatch / Cloud Monitoring: $100-200/month
- BigQuery / Redshift: $200-500/month
- Grafana Cloud (optional): $50-100/month
- Log storage: $50-100/month
- Alerting: Included
- **Total: $400-900/month**

**Still 90%+ cheaper than commercial password managers!**

---

## Next Steps

1. **Week 1:** Implement cloud-native monitoring
2. **Week 2:** Set up event log analytics
3. **Week 3:** Build custom dashboards
4. **Week 4:** Automate reporting

**Then:** Monitor, refine, and optimize continuously

---

## Related Documentation

- 📈 **[Monitoring Guide](../operations/MONITORING.md)** - Infrastructure monitoring
- 🔒 **[Security Guide](../operations/SECURITY.md)** - Security best practices
- 📊 **[Scaling Guide](../operations/SCALING_GUIDE.md)** - Scale to 100,000+ users
- 👥 **[Organizations Guide](../organizations/ORGANIZATIONS_GUIDE.md)** - Team features

---

## Conclusion

**Transform your Vaultwarden deployment into a data-driven security platform.**

**Key Takeaways:**
1. ✅ Multiple data sources available (events, logs, metrics)
2. ✅ Multiple implementation options (cloud-native to full analytics)
3. ✅ Start simple, scale as needed
4. ✅ Costs $15-900/month depending on scale
5. ✅ 4-week implementation for complete solution
6. ✅ Enables security insights, compliance, and optimization

**Recommended Action:** Start with cloud-native monitoring (Week 1), then expand based on needs.

---

**Document Version:** 1.0  
**Last Updated:** November 5, 2025  
**Next Review:** February 2026

**Questions?** adrian207@gmail.com

