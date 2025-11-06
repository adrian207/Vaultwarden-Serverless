# Quick Start Guide - DevOps Secrets Management

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Date:** November 5, 2025  
**Status:** Phase 1 - Development Started

## 🚀 Get Started in 5 Minutes

This guide will get you up and running with the DevOps Secrets Management API.

---

## Prerequisites

- **Python 3.11+**
- **PostgreSQL 14+** (or use existing Vaultwarden database)
- **Git**
- **Terminal/Command Line**

---

## Step 1: Initial Setup (2 minutes)

```bash
# Navigate to the secrets management directory
cd backend/secrets-management

# Run the automated setup script
chmod +x setup.sh
./setup.sh
```

The setup script will:
- ✅ Check prerequisites
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Generate secure secrets
- ✅ Create .env configuration file
- ✅ Set up project structure

---

## Step 2: Configure Environment (1 minute)

The setup script creates a `.env` file with secure defaults. Review and update if needed:

```bash
# Edit .env file
nano .env  # or use your preferred editor

# Key settings to verify:
# - DATABASE_URL: Your PostgreSQL connection string
# - SECRET_KEY: Auto-generated (secure)
# - ENCRYPTION_KEY: Auto-generated (secure)
# - VAULTWARDEN_URL: URL of your Vaultwarden instance
```

---

## Step 3: Run Database Migrations (1 minute)

```bash
# Option 1: Using psql directly
psql -U vaultwarden -d vaultwarden -f database/migrations/001_initial_schema.sql

# Option 2: Using connection string from .env
psql $(grep DATABASE_URL .env | cut -d '=' -f2) -f database/migrations/001_initial_schema.sql
```

This creates all necessary tables:
- `service_accounts` - Service account definitions
- `api_keys` - API key authentication  
- `secrets_metadata` - Secret metadata
- `secret_versions` - Version history
- `rotation_policies` - Automatic rotation
- `secret_audit_log` - Audit trail

---

## Step 4: Start the API Server (1 minute)

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start development server
python -m uvicorn api.main:app --reload --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

---

## Step 5: Test the API

### 5a. Health Check

```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "secrets-management-api",
  "version": "1.0.0"
}
```

### 5b. API Documentation

Open in your browser:
```
http://localhost:8001/docs
```

You'll see interactive Swagger UI with all API endpoints.

---

## 🎯 Your First Secret

### Create a Service Account

```bash
curl -X POST http://localhost:8001/api/v1/service-accounts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-app",
    "description": "My application service account",
    "permissions": {
      "paths": ["development/*"],
      "actions": ["read", "write"]
    }
  }'
```

Response includes an API key:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "my-app",
  "api_key": "vw_svc_abc123xyz...",
  "created_at": "2025-11-05T10:00:00Z"
}
```

**⚠️ Save this API key! It's only shown once.**

### Store a Secret

```bash
curl -X POST http://localhost:8001/api/v1/secrets/development/database-url \
  -H "Authorization: Bearer vw_svc_abc123xyz..." \
  -H "Content-Type: application/json" \
  -d '{
    "value": "postgresql://user:pass@localhost/mydb",
    "description": "Development database connection",
    "metadata": {
      "environment": "development",
      "owner": "backend-team"
    }
  }'
```

### Retrieve a Secret

```bash
curl http://localhost:8001/api/v1/secrets/development/database-url \
  -H "Authorization: Bearer vw_svc_abc123xyz..."
```

Response:
```json
{
  "path": "development/database-url",
  "value": "postgresql://user:pass@localhost/mydb",
  "version": 1,
  "description": "Development database connection",
  "metadata": {
    "environment": "development",
    "owner": "backend-team"
  },
  "created_at": "2025-11-05T10:05:00Z"
}
```

---

## 📖 Next Steps

### Explore the API

Visit `http://localhost:8001/docs` to explore all endpoints:

**Service Accounts:**
- Create, list, update, delete service accounts
- Generate and revoke API keys

**Secrets:**
- Create, read, update, delete secrets
- List secrets with prefix matching
- Get secret version history
- Rollback to previous versions

**Audit:**
- View secret access logs
- Generate audit reports
- Track service account activity

### Phase 1 Development Tasks

The project is in **Phase 1: Core API & Authentication** (Weeks 1-2).

**Completed:** ✅
- Project structure setup
- Database schema design
- Configuration management
- Development environment

**In Progress:**
- [ ] Implement API routes (see `api/routes/`)
- [ ] Authentication middleware (see `api/middleware/auth.py`)
- [ ] Rate limiting (see `api/middleware/rate_limit.py`)
- [ ] Service account management
- [ ] Secret CRUD operations
- [ ] Audit logging
- [ ] Unit tests

**To Do:**
- [ ] API documentation
- [ ] Integration tests
- [ ] Performance optimization

---

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies (already in requirements.txt)
pytest

# With coverage report
pytest --cov=api --cov=services --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Manual Testing

Use the Swagger UI at `http://localhost:8001/docs` for interactive testing.

---

## 🐛 Troubleshooting

### Database Connection Errors

**Issue:** `could not connect to server: Connection refused`

**Solution:**
1. Check PostgreSQL is running: `pg_isready`
2. Verify DATABASE_URL in `.env`
3. Check PostgreSQL logs: `tail -f /var/log/postgresql/*.log`

### Import Errors

**Issue:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
1. Activate virtual environment: `source venv/bin/activate`
2. Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use

**Issue:** `Address already in use`

**Solution:**
1. Check what's using port 8001: `lsof -i :8001`
2. Kill the process: `kill -9 [PID]`
3. Or use a different port: `uvicorn api.main:app --port 8002`

---

## 📁 Project Structure

```
backend/secrets-management/
├── api/                       # FastAPI application
│   ├── main.py               # Entry point
│   ├── routes/               # API endpoints
│   │   ├── secrets.py        # Secret management
│   │   ├── service_accounts.py
│   │   ├── rotation.py
│   │   └── audit.py
│   ├── middleware/           # Request middleware
│   │   ├── auth.py           # Authentication
│   │   ├── rate_limit.py     # Rate limiting
│   │   └── logging.py        # Request logging
│   └── schemas/              # Pydantic models
│       ├── secret.py
│       └── service_account.py
├── database/
│   └── migrations/           # SQL schema migrations
│       └── 001_initial_schema.sql
├── config/
│   └── settings.py           # Configuration management
├── services/                 # Business logic
├── tests/                    # Unit & integration tests
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script
├── README.md                 # Full documentation
└── QUICKSTART.md            # This file
```

---

## 🎓 Learning Resources

### API Documentation
- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **OpenAPI JSON:** http://localhost:8001/openapi.json

### Code Examples
See `docs/EXAMPLES.md` for:
- CI/CD integration examples
- Rotation policy configuration
- Client library usage
- Common patterns

### Complete Guide
See `docs/features/DEVOPS_SECRETS_MANAGEMENT.md` for:
- Complete technical specification
- Architecture details
- Security considerations
- Production deployment

---

## 💡 Tips & Best Practices

### Development

1. **Use virtual environment:** Always activate venv before working
2. **Format code:** Run `black .` before committing
3. **Check types:** Run `mypy api/` to catch type errors
4. **Write tests:** Maintain 80%+ code coverage

### Security

1. **Never commit .env:** It contains sensitive secrets
2. **Rotate API keys:** Regularly rotate service account keys
3. **Use HTTPS:** In production, always use TLS
4. **Audit logs:** Review audit logs regularly

### Performance

1. **Connection pooling:** Configure DB pool size based on load
2. **Rate limiting:** Adjust limits based on your needs
3. **Caching:** Consider Redis for high-traffic scenarios
4. **Monitoring:** Enable Prometheus metrics

---

## 📊 Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8001/health

# Readiness (includes dependencies)
curl http://localhost:8001/ready
```

### Metrics (Prometheus)

```bash
# Prometheus metrics
curl http://localhost:8001/metrics
```

Key metrics:
- `api_requests_total` - Total requests
- `api_request_duration_seconds` - Request latency
- `api_errors_total` - Error count
- `secrets_total` - Total secrets managed
- `rotation_success_total` - Successful rotations

---

## 🤝 Getting Help

### Documentation
- [README.md](README.md) - Full documentation
- [API.md](docs/API.md) - API reference
- [Complete Implementation Guide](../../docs/features/DEVOPS_SECRETS_MANAGEMENT.md)

### Support
- **Email:** adrian207@gmail.com
- **Issues:** Open a GitHub issue
- **Discussions:** GitHub Discussions

---

## ✅ Checklist

Use this checklist to ensure everything is working:

- [ ] Setup script completed successfully
- [ ] Virtual environment activated
- [ ] .env file configured
- [ ] Database migrations applied
- [ ] API server starts without errors
- [ ] Health check returns "healthy"
- [ ] Can access Swagger UI at /docs
- [ ] Created first service account
- [ ] Stored first secret
- [ ] Retrieved secret successfully
- [ ] Audit log shows activity

---

**Ready to build? Let's go! 🚀**

**Questions?** Read [README.md](README.md) or contact adrian207@gmail.com

