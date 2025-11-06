# DevOps Secrets Management Module

**Author:** Adrian Johnson <adrian207@gmail.com>  
**Status:** Phase 1 - In Development  
**Timeline:** 6-8 weeks  
**Investment:** $30k-50k

## Overview

API-first secrets management system that replaces HashiCorp Vault at 10% of the cost.

**Key Capabilities:**
- REST API for programmatic secret access
- Service accounts with API key authentication
- Automatic secret rotation
- Secret versioning and rollback
- CI/CD integration
- Kubernetes secrets operator
- Developer CLI tool

---

## Project Structure

```
backend/secrets-management/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── config/
│   ├── settings.py               # Configuration management
│   └── database.py               # Database connection
├── database/
│   ├── migrations/               # Database schema migrations
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_service_accounts.sql
│   │   ├── 003_secret_versions.sql
│   │   └── 004_rotation_policies.sql
│   └── models.py                 # SQLAlchemy models
├── api/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── routes/
│   │   ├── secrets.py            # Secret management endpoints
│   │   ├── service_accounts.py  # Service account endpoints
│   │   ├── rotation.py           # Rotation policy endpoints
│   │   └── audit.py              # Audit log endpoints
│   ├── middleware/
│   │   ├── auth.py               # API key authentication
│   │   ├── rate_limit.py         # Rate limiting
│   │   └── logging.py            # Request logging
│   └── schemas/
│       ├── secret.py             # Pydantic models for secrets
│       ├── service_account.py    # Pydantic models for accounts
│       └── rotation.py           # Pydantic models for rotation
├── services/
│   ├── secret_manager.py         # Core secret operations
│   ├── rotation_engine.py        # Automatic rotation logic
│   ├── versioning.py             # Secret version management
│   └── encryption.py             # Encryption utilities
├── integrations/
│   ├── github_actions.py         # GitHub Actions plugin
│   ├── gitlab_ci.py              # GitLab CI plugin
│   └── kubernetes.py             # K8s operator base
├── cli/
│   ├── setup.py                  # CLI package setup
│   ├── vw_cli/
│   │   ├── __init__.py
│   │   ├── main.py               # CLI entry point
│   │   ├── commands/
│   │   │   ├── get.py            # Get secret command
│   │   │   ├── set.py            # Set secret command
│   │   │   ├── list.py           # List secrets command
│   │   │   └── rotate.py         # Rotate secret command
│   │   └── config.py             # CLI configuration
├── tests/
│   ├── test_api.py               # API endpoint tests
│   ├── test_rotation.py          # Rotation tests
│   ├── test_versioning.py        # Versioning tests
│   └── test_integration.py       # Integration tests
└── docs/
    ├── API.md                    # API documentation
    ├── SETUP.md                  # Setup guide
    └── EXAMPLES.md               # Usage examples
```

---

## Phase 1: Core API & Authentication (Weeks 1-2)

### Sprint 1 (Week 1)
- [x] Set up project structure
- [ ] Database schema design and migrations
- [ ] Core API application (FastAPI)
- [ ] Service account model
- [ ] API key generation and validation
- [ ] Basic authentication middleware

### Sprint 2 (Week 2)
- [ ] Secrets API endpoints (CRUD)
- [ ] Rate limiting middleware
- [ ] Audit logging
- [ ] Unit tests (80%+ coverage)
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Development environment setup

---

## Quick Start (Development)

### Prerequisites
```bash
# Python 3.11+
python --version

# PostgreSQL 14+ (or use existing Vaultwarden DB)
psql --version

# Docker (for local testing)
docker --version
```

### Setup

```bash
# Navigate to secrets management module
cd backend/secrets-management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database connection string

# Run database migrations
python -m alembic upgrade head

# Start development server
uvicorn api.main:app --reload --port 8001
```

### Test API
```bash
# Access API documentation
open http://localhost:8001/docs

# Create a service account
curl -X POST http://localhost:8001/api/v1/service-accounts \
  -H "Content-Type: application/json" \
  -d '{"name": "test-app", "permissions": {"paths": ["dev/*"]}}'

# Store a secret
curl -X POST http://localhost:8001/api/v1/secrets/dev/database-url \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"value": "postgresql://localhost/test"}'

# Retrieve a secret
curl http://localhost:8001/api/v1/secrets/dev/database-url \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## Phase 2: Secret Versioning (Weeks 3-4)

### Features
- [ ] Secret version tracking
- [ ] Version history API
- [ ] Rollback functionality
- [ ] Version metadata
- [ ] Automatic version pruning

---

## Phase 3: Automatic Rotation (Weeks 5-6)

### Features
- [ ] Rotation policy engine
- [ ] Database rotation plugins (PostgreSQL, MySQL)
- [ ] Cloud provider rotation (AWS, GCP)
- [ ] Health check system
- [ ] Automatic rollback on failure

---

## Phase 4: Integrations (Weeks 7-8)

### Features
- [ ] GitHub Actions integration
- [ ] GitLab CI integration
- [ ] Kubernetes operator
- [ ] Developer CLI tool
- [ ] Secret scanning tool

---

## API Endpoints

### Service Accounts
```
POST   /api/v1/service-accounts           # Create service account
GET    /api/v1/service-accounts           # List service accounts
GET    /api/v1/service-accounts/:id       # Get service account
PUT    /api/v1/service-accounts/:id       # Update service account
DELETE /api/v1/service-accounts/:id       # Delete service account
POST   /api/v1/service-accounts/:id/keys  # Generate API key
DELETE /api/v1/service-accounts/:id/keys/:key_id # Revoke API key
```

### Secrets
```
GET    /api/v1/secrets                    # List secrets (metadata)
GET    /api/v1/secrets/:path              # Get secret value
POST   /api/v1/secrets/:path              # Create/update secret
DELETE /api/v1/secrets/:path              # Delete secret
GET    /api/v1/secrets/:path/versions     # Get version history
POST   /api/v1/secrets/:path/rollback     # Rollback to version
```

### Rotation
```
GET    /api/v1/rotation-policies          # List rotation policies
POST   /api/v1/rotation-policies          # Create rotation policy
GET    /api/v1/rotation-policies/:id      # Get rotation policy
PUT    /api/v1/rotation-policies/:id      # Update rotation policy
DELETE /api/v1/rotation-policies/:id      # Delete rotation policy
POST   /api/v1/secrets/:path/rotate       # Trigger rotation
```

### Audit
```
GET    /api/v1/audit/secrets/:path        # Secret access log
GET    /api/v1/audit/service-accounts/:id # Service account activity
GET    /api/v1/audit/report               # Generate audit report
```

---

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions small and focused

### Testing
- Write unit tests for all new features
- Maintain 80%+ code coverage
- Write integration tests for API endpoints
- Test error handling and edge cases

### Security
- Never log secret values
- Use constant-time comparison for API keys
- Validate all input data
- Rate limit all endpoints
- Implement proper access controls

---

## Database Schema

See `database/migrations/` for complete SQL schemas.

### Key Tables
- `service_accounts` - Service account definitions
- `api_keys` - API key authentication
- `secrets_metadata` - Secret paths and metadata (values stored in Vaultwarden ciphers)
- `secret_versions` - Version history
- `rotation_policies` - Automatic rotation configuration
- `secret_audit_log` - Access audit trail

---

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/vaultwarden

# API Settings
API_HOST=0.0.0.0
API_PORT=8001
API_KEY_LENGTH=32

# Rate Limiting
RATE_LIMIT_PER_SECOND=100
RATE_LIMIT_BURST=200

# Security
SECRET_KEY=your-secret-key-here
API_KEY_SALT=your-salt-here

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/secrets-api.log
```

---

## Monitoring

### Health Check
```bash
GET /health
```

### Metrics (Prometheus)
```bash
GET /metrics
```

### Key Metrics
- `api_requests_total` - Total API requests
- `api_request_duration_seconds` - Request latency
- `api_errors_total` - API errors
- `secrets_total` - Total secrets managed
- `rotation_success_total` - Successful rotations
- `rotation_failure_total` - Failed rotations

---

## Next Steps

1. **Review this README** ✅
2. **Run `setup.sh`** to initialize project
3. **Review database migrations** in `database/migrations/`
4. **Start development server** with `uvicorn`
5. **Test API endpoints** using Swagger UI
6. **Begin Sprint 1 tasks**

---

## Resources

- [Complete Implementation Guide](../../docs/features/DEVOPS_SECRETS_MANAGEMENT.md)
- [API Documentation](docs/API.md)
- [Setup Guide](docs/SETUP.md)
- [Usage Examples](docs/EXAMPLES.md)

---

## Support

**Questions?** adrian207@gmail.com  
**Issues?** Open a GitHub issue  
**Discussions?** GitHub Discussions

---

**Let's build the future of secrets management! 🚀**

