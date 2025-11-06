#!/bin/bash
# DevOps Secrets Management - Setup Script
# Author: Adrian Johnson <adrian207@gmail.com>
# Date: 2025-11-05

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   Vaultwarden DevOps Secrets Management - Setup              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# CHECKS
# ============================================================================

echo "🔍 Checking prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client not found (optional, but recommended)"
else
    PSQL_VERSION=$(psql --version | awk '{print $3}')
    echo "✅ PostgreSQL $PSQL_VERSION found"
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    echo "✅ Docker $DOCKER_VERSION found"
else
    echo "⚠️  Docker not found (optional, but useful for testing)"
fi

echo ""

# ============================================================================
# VIRTUAL ENVIRONMENT
# ============================================================================

echo "📦 Setting up Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate

echo "✅ Virtual environment activated"
echo ""

# ============================================================================
# DEPENDENCIES
# ============================================================================

echo "📚 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

echo "⚙️  Setting up environment configuration..."

if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and update the following values:"
    echo "   - SECRET_KEY (generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\")"
    echo "   - API_KEY_SALT (generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\")"
    echo "   - ENCRYPTION_KEY (generate with: python -c \"import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())\")"
    echo "   - DATABASE_URL (if different from default)"
    echo ""
else
    echo "✅ .env file already exists"
fi

# ============================================================================
# GENERATE SECRETS (if needed)
# ============================================================================

if grep -q "your-secret-key-here-change-me" .env 2>/dev/null; then
    echo "🔐 Generating secure secrets..."
    
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    API_KEY_SALT=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    ENCRYPTION_KEY=$(python3 -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())")
    
    # Update .env file (works on both macOS and Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        sed -i '' "s/API_KEY_SALT=.*/API_KEY_SALT=$API_KEY_SALT/" .env
        sed -i '' "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$ENCRYPTION_KEY/" .env
    else
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        sed -i "s/API_KEY_SALT=.*/API_KEY_SALT=$API_KEY_SALT/" .env
        sed -i "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$ENCRYPTION_KEY/" .env
    fi
    
    echo "✅ Secure secrets generated and saved to .env"
fi

echo ""

# ============================================================================
# DATABASE SETUP
# ============================================================================

echo "🗄️  Database setup..."
echo ""
echo "Run the database migrations with:"
echo "  psql -U vaultwarden -d vaultwarden -f database/migrations/001_initial_schema.sql"
echo ""
echo "Or if using a different database:"
echo "  psql -U [username] -d [database] -f database/migrations/001_initial_schema.sql"
echo ""

read -p "Do you want to run database migrations now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Extract database details from .env
    DATABASE_URL=$(grep DATABASE_URL .env | cut -d '=' -f2)
    
    if [[ $DATABASE_URL == postgresql://* ]]; then
        # Parse DATABASE_URL
        # postgresql://user:pass@host:port/database
        DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\(.*\)/\1/p')
        
        echo "Running migration on $DB_HOST:$DB_PORT/$DB_NAME as $DB_USER..."
        PGPASSWORD=$(echo $DATABASE_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p') \
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f database/migrations/001_initial_schema.sql
        
        if [ $? -eq 0 ]; then
            echo "✅ Database migrations completed successfully"
        else
            echo "❌ Database migration failed"
            echo "   Please run manually or check your DATABASE_URL"
        fi
    else
        echo "⚠️  Could not parse DATABASE_URL. Please run migrations manually."
    fi
fi

echo ""

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

echo "📁 Creating project structure..."

# Create necessary directories
mkdir -p api/routes
mkdir -p api/middleware
mkdir -p api/schemas
mkdir -p services
mkdir -p integrations
mkdir -p cli/vw_cli/commands
mkdir -p tests
mkdir -p docs
mkdir -p logs

# Create __init__.py files
touch api/__init__.py
touch api/routes/__init__.py
touch api/middleware/__init__.py
touch api/schemas/__init__.py
touch services/__init__.py
touch integrations/__init__.py
touch cli/vw_cli/__init__.py
touch cli/vw_cli/commands/__init__.py

echo "✅ Project structure created"
echo ""

# ============================================================================
# DONE
# ============================================================================

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   ✅ Setup Complete!                                          ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "1. Review and update .env file with your configuration"
echo "2. Run database migrations (if not done already)"
echo "3. Start the development server:"
echo "     python -m uvicorn api.main:app --reload --port 8001"
echo ""
echo "4. Access API documentation:"
echo "     http://localhost:8001/docs"
echo ""
echo "5. Test health endpoint:"
echo "     curl http://localhost:8001/health"
echo ""
echo "📖 Next Steps:"
echo "   - Read README.md for detailed information"
echo "   - Review docs/API.md for API documentation"
echo "   - Check database/migrations/ for schema details"
echo ""
echo "💡 Development Tips:"
echo "   - Activate venv: source venv/bin/activate"
echo "   - Run tests: pytest"
echo "   - Format code: black ."
echo "   - Check types: mypy api/"
echo ""
echo "📧 Questions? adrian207@gmail.com"
echo ""

