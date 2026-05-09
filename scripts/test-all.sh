#!/bin/bash

# NeoNova Test Runner Script
# Runs all tests for both backend and frontend

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

# Run backend tests
run_backend_tests() {
    log "Running backend tests..."
    
    cd "$BACKEND_DIR"
    
    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        error "Virtual environment not found. Run setup first."
        return 1
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run tests with coverage
    log "Running Python tests with coverage..."
    if pytest --cov=src --cov-report=term-missing --cov-report=html; then
        success "Backend tests passed!"
        log "Coverage report generated in htmlcov/"
        return 0
    else
        error "Backend tests failed!"
        return 1
    fi
}

# Run frontend tests
run_frontend_tests() {
    log "Running frontend tests..."
    
    cd "$FRONTEND_DIR"
    
    # Check if node_modules exists
    if [[ ! -d "node_modules" ]]; then
        error "Node modules not found. Run npm install first."
        return 1
    fi
    
    # Check if test script exists in package.json
    if ! grep -q '"test"' package.json; then
        warning "No test script defined in frontend package.json. Skipping frontend tests."
        warning "Frontend build validation will be performed instead."
        
        # Validate frontend build instead
        log "Running frontend build validation..."
        if npm run build; then
            success "Frontend build validation passed!"
            return 0
        else
            error "Frontend build validation failed!"
            return 1
        fi
    fi
    
    # Run tests
    log "Running JavaScript/TypeScript tests..."
    if npm test; then
        success "Frontend tests passed!"
        return 0
    else
        error "Frontend tests failed!"
        return 1
    fi
}

# Run linting
run_linting() {
    log "Running code quality checks..."
    
    local backend_lint_success=true
    local frontend_lint_success=true
    
    # Backend linting
    cd "$BACKEND_DIR"
    if [[ -d "venv" ]]; then
        source venv/bin/activate
        
        log "Running Python linting..."
        if command -v black >/dev/null 2>&1; then
            black --check src/ tests/ || backend_lint_success=false
        fi
        
        if command -v isort >/dev/null 2>&1; then
            isort --check-only src/ tests/ || backend_lint_success=false
        fi
        
        if command -v mypy >/dev/null 2>&1; then
            mypy src/ || backend_lint_success=false
        fi
    fi
    
    # Frontend linting
    cd "$FRONTEND_DIR"
    if [[ -d "node_modules" ]]; then
        log "Running JavaScript/TypeScript linting..."
        npm run lint || frontend_lint_success=false
    fi
    
    if [[ "$backend_lint_success" == true ]] && [[ "$frontend_lint_success" == true ]]; then
        success "All linting checks passed!"
        return 0
    else
        error "Some linting checks failed!"
        return 1
    fi
}

# Main function
main() {
    local run_backend=true
    local run_frontend=true
    local run_lint=false
    local exit_code=0
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backend-only)
                run_frontend=false
                shift
                ;;
            --frontend-only)
                run_backend=false
                shift
                ;;
            --with-lint)
                run_lint=true
                shift
                ;;
            --help|-h)
                echo "NeoNova Test Runner"
                echo ""
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --backend-only   Run only backend tests"
                echo "  --frontend-only  Run only frontend tests"
                echo "  --with-lint      Include linting checks"
                echo "  --help, -h       Show this help message"
                echo ""
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    log "Starting test suite..."
    
    # Run linting first if requested
    if [[ "$run_lint" == true ]]; then
        if ! run_linting; then
            exit_code=1
        fi
    fi
    
    # Run backend tests
    if [[ "$run_backend" == true ]]; then
        if ! run_backend_tests; then
            exit_code=1
        fi
    fi
    
    # Run frontend tests
    if [[ "$run_frontend" == true ]]; then
        if ! run_frontend_tests; then
            exit_code=1
        fi
    fi
    
    # Summary
    if [[ $exit_code -eq 0 ]]; then
        success "All tests completed successfully!"
    else
        error "Some tests failed!"
    fi
    
    exit $exit_code
}

# Run main function with all arguments
main "$@"