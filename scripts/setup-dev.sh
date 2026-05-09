#!/bin/bash

# NeoNova Development Setup Script
# Sets up the development environment for both backend and frontend

set -e

# Configuration
BACKEND_DIR="$(dirname "$0")/../backend"
FRONTEND_DIR="$(dirname "$0")/../frontend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Python
    if ! command -v python3 >/dev/null 2>&1; then
        error "Python 3 is not installed. Please install Python 3.12 or later."
        exit 1
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2)
    log "Found Python $python_version"
    
    # Check Node.js
    if ! command -v node >/dev/null 2>&1; then
        error "Node.js is not installed. Please install Node.js 18 or later."
        exit 1
    fi
    
    local node_version=$(node --version)
    log "Found Node.js $node_version"
    
    # Check npm
    if ! command -v npm >/dev/null 2>&1; then
        error "npm is not installed. Please install npm."
        exit 1
    fi
    
    local npm_version=$(npm --version)
    log "Found npm $npm_version"
    
    # Check PostgreSQL (optional)
    if command -v psql >/dev/null 2>&1; then
        local pg_version=$(psql --version | cut -d' ' -f3)
        log "Found PostgreSQL $pg_version"
    else
        warning "PostgreSQL not found. You'll need to install it for the backend database."
    fi
    
    success "Prerequisites check completed!"
}

# Setup backend
setup_backend() {
    log "Setting up backend..."
    
    cd "$BACKEND_DIR"
    
    # Create virtual environment
    if [[ ! -d "venv" ]]; then
        log "Creating Python virtual environment..."
        python3 -m venv venv
    else
        log "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    log "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    log "Installing Python dependencies..."
    pip install -e .[dev]
    
    # Setup environment file
    if [[ ! -f ".env" ]]; then
        log "Creating .env file from template..."
        cp .env.example .env
        warning "Please edit .env file with your configuration:"
        warning "  - Set DATABASE_URL for your PostgreSQL database"
        warning "  - Set OPENAI_API_KEY for AI functionality"
        warning "  - Set SECRET_KEY for JWT authentication"
    else
        log ".env file already exists"
    fi
    
    success "Backend setup completed!"
}

# Setup frontend
setup_frontend() {
    log "Setting up frontend..."
    
    cd "$FRONTEND_DIR"
    
    # Install dependencies
    log "Installing Node.js dependencies..."
    npm install
    
    # Setup environment file
    if [[ ! -f ".env" ]]; then
        log "Creating .env file from template..."
        cp .env.example .env
        warning "Please edit .env file with your configuration:"
        warning "  - Set VITE_API_BASE_URL to your backend URL (default: http://localhost:8000)"
    else
        log ".env file already exists"
    fi
    
    success "Frontend setup completed!"
}

# Setup database
setup_database() {
    log "Setting up database..."
    
    cd "$BACKEND_DIR"
    
    # Check if PostgreSQL is available
    if ! command -v createdb >/dev/null 2>&1; then
        warning "PostgreSQL tools not found. Skipping database setup."
        warning "Please install PostgreSQL and create a database manually."
        return 0
    fi
    
    # Check if database exists
    local db_name="neonova_dev"
    if psql -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        log "Database '$db_name' already exists"
    else
        log "Creating database '$db_name'..."
        createdb "$db_name" || {
            warning "Failed to create database. You may need to:"
            warning "  1. Start PostgreSQL service"
            warning "  2. Create the database manually: createdb $db_name"
            return 0
        }
        success "Database '$db_name' created!"
    fi
    
    # Run migrations if virtual environment exists
    if [[ -d "venv" ]]; then
        source venv/bin/activate
        
        # Check if alembic is available
        if command -v alembic >/dev/null 2>&1; then
            log "Running database migrations..."
            alembic upgrade head || {
                warning "Failed to run migrations. You may need to:"
                warning "  1. Configure DATABASE_URL in .env file"
                warning "  2. Run migrations manually: alembic upgrade head"
            }
        else
            warning "Alembic not found. Install backend dependencies first."
        fi
    fi
    
    success "Database setup completed!"
}

# Run tests to verify setup
verify_setup() {
    log "Verifying setup..."
    
    local backend_ok=true
    local frontend_ok=true
    
    # Test backend
    cd "$BACKEND_DIR"
    if [[ -d "venv" ]]; then
        source venv/bin/activate
        log "Running backend tests..."
        if pytest tests/ -x -q; then
            success "Backend tests passed!"
        else
            error "Backend tests failed!"
            backend_ok=false
        fi
    else
        warning "Backend virtual environment not found"
        backend_ok=false
    fi
    
    # Test frontend
    cd "$FRONTEND_DIR"
    if [[ -d "node_modules" ]]; then
        log "Checking frontend build..."
        if npm run build >/dev/null 2>&1; then
            success "Frontend builds successfully!"
        else
            error "Frontend build failed!"
            frontend_ok=false
        fi
    else
        warning "Frontend node_modules not found"
        frontend_ok=false
    fi
    
    if [[ "$backend_ok" == true ]] && [[ "$frontend_ok" == true ]]; then
        success "Setup verification completed successfully!"
        return 0
    else
        error "Setup verification failed!"
        return 1
    fi
}

# Show next steps
show_next_steps() {
    log "Setup completed! Next steps:"
    echo ""
    echo "1. Configure your environment files:"
    echo "   - Backend: $BACKEND_DIR/.env"
    echo "   - Frontend: $FRONTEND_DIR/.env"
    echo ""
    echo "2. Start the services:"
    echo "   ./scripts/manage-services.sh start"
    echo ""
    echo "3. Access the application:"
    echo "   - Frontend: http://localhost:5173"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo ""
    echo "4. Run tests:"
    echo "   ./scripts/test-all.sh"
    echo ""
    echo "For more information, see the README.md file."
}

# Main function
main() {
    local skip_db=false
    local skip_verify=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-db)
                skip_db=true
                shift
                ;;
            --skip-verify)
                skip_verify=true
                shift
                ;;
            --help|-h)
                echo "NeoNova Development Setup"
                echo ""
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --skip-db       Skip database setup"
                echo "  --skip-verify   Skip setup verification"
                echo "  --help, -h      Show this help message"
                echo ""
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    log "Starting NeoNova development setup..."
    
    # Run setup steps
    check_prerequisites
    setup_backend
    setup_frontend
    
    if [[ "$skip_db" != true ]]; then
        setup_database
    fi
    
    if [[ "$skip_verify" != true ]]; then
        verify_setup
    fi
    
    show_next_steps
    
    success "Development environment setup completed!"
}

# Run main function with all arguments
main "$@"