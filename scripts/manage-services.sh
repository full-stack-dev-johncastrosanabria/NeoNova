#!/bin/bash

# NeoNova Service Management Script
# Manages backend and frontend services with health checks

set -e

# Configuration
BACKEND_DIR="$(dirname "$0")/../backend"
FRONTEND_DIR="$(dirname "$0")/../frontend"
LOG_DIR="$(dirname "$0")/../logs"
BACKEND_PORT=8000
FRONTEND_PORT=5173
BACKEND_PID_FILE="$LOG_DIR/backend.pid"
FRONTEND_PID_FILE="$LOG_DIR/frontend.pid"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create logs directory
mkdir -p "$LOG_DIR"

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

# Cleanup function - stops all services on exit
cleanup() {
    log "Cleaning up services..."
    stop_services
    exit 0
}

# Trap signals to ensure cleanup
trap cleanup SIGINT SIGTERM EXIT

# Check if a service is running on a port
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Get PID from file
get_pid() {
    local pid_file=$1
    if [[ -f "$pid_file" ]]; then
        cat "$pid_file"
    else
        echo ""
    fi
}

# Check if process is running
is_process_running() {
    local pid=$1
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Health check for backend
check_backend_health() {
    local max_attempts=30
    local attempt=1
    
    log "Checking backend health..."
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s -f "http://localhost:$BACKEND_PORT/health" >/dev/null 2>&1; then
            success "Backend is healthy (attempt $attempt/$max_attempts)"
            return 0
        fi
        
        if [[ $attempt -eq $max_attempts ]]; then
            error "Backend health check failed after $max_attempts attempts"
            return 1
        fi
        
        log "Backend not ready yet (attempt $attempt/$max_attempts), waiting..."
        sleep 2
        ((attempt++))
    done
}

# Health check for frontend
check_frontend_health() {
    local max_attempts=30
    local attempt=1
    
    log "Checking frontend health..."
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s -f "http://localhost:$FRONTEND_PORT" >/dev/null 2>&1; then
            success "Frontend is healthy (attempt $attempt/$max_attempts)"
            return 0
        fi
        
        if [[ $attempt -eq $max_attempts ]]; then
            error "Frontend health check failed after $max_attempts attempts"
            return 1
        fi
        
        log "Frontend not ready yet (attempt $attempt/$max_attempts), waiting..."
        sleep 2
        ((attempt++))
    done
}

# Start backend service
start_backend() {
    log "Starting backend service..."
    
    # Check if already running
    local existing_pid=$(get_pid "$BACKEND_PID_FILE")
    if is_process_running "$existing_pid"; then
        warning "Backend already running with PID $existing_pid"
        return 0
    fi
    
    # Check if port is occupied by another process
    if check_port $BACKEND_PORT; then
        error "Port $BACKEND_PORT is already in use by another process"
        return 1
    fi
    
    # Change to backend directory
    cd "$BACKEND_DIR"
    
    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        log "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    
    # Install dependencies if needed
    if [[ ! -f "venv/pyvenv.cfg" ]] || [[ pyproject.toml -nt venv/pyvenv.cfg ]]; then
        log "Installing Python dependencies..."
        pip install -e .[dev]
    fi
    
    # Check if .env exists
    if [[ ! -f ".env" ]]; then
        warning ".env file not found, copying from .env.example"
        cp .env.example .env
        warning "Please edit .env file with your configuration"
    fi
    
    # Start the backend service
    log "Launching FastAPI server..."
    nohup uvicorn src.main:app --reload --host 0.0.0.0 --port $BACKEND_PORT \
        > "$LOG_DIR/backend.log" 2>&1 &
    
    local backend_pid=$!
    echo $backend_pid > "$BACKEND_PID_FILE"
    
    success "Backend started with PID $backend_pid"
    
    # Health check
    if check_backend_health; then
        success "Backend is running and healthy at http://localhost:$BACKEND_PORT"
        log "API Documentation: http://localhost:$BACKEND_PORT/docs"
    else
        error "Backend failed health check"
        return 1
    fi
}

# Start frontend service
start_frontend() {
    log "Starting frontend service..."
    
    # Check if already running
    local existing_pid=$(get_pid "$FRONTEND_PID_FILE")
    if is_process_running "$existing_pid"; then
        warning "Frontend already running with PID $existing_pid"
        return 0
    fi
    
    # Check if port is occupied by another process
    if check_port $FRONTEND_PORT; then
        error "Port $FRONTEND_PORT is already in use by another process"
        return 1
    fi
    
    # Change to frontend directory
    cd "$FRONTEND_DIR"
    
    # Install dependencies if needed
    if [[ ! -d "node_modules" ]] || [[ package.json -nt node_modules ]]; then
        log "Installing Node.js dependencies..."
        npm install
    fi
    
    # Check if .env exists
    if [[ ! -f ".env" ]]; then
        warning ".env file not found, copying from .env.example"
        cp .env.example .env
        warning "Please edit .env file with your configuration"
    fi
    
    # Start the frontend service
    log "Launching Vite development server..."
    nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
    
    local frontend_pid=$!
    echo $frontend_pid > "$FRONTEND_PID_FILE"
    
    success "Frontend started with PID $frontend_pid"
    
    # Health check
    if check_frontend_health; then
        success "Frontend is running and healthy at http://localhost:$FRONTEND_PORT"
    else
        error "Frontend failed health check"
        return 1
    fi
}

# Stop backend service
stop_backend() {
    local pid=$(get_pid "$BACKEND_PID_FILE")
    
    if is_process_running "$pid"; then
        log "Stopping backend service (PID: $pid)..."
        kill "$pid"
        
        # Wait for graceful shutdown
        local attempts=10
        while [[ $attempts -gt 0 ]] && is_process_running "$pid"; do
            sleep 1
            ((attempts--))
        done
        
        # Force kill if still running
        if is_process_running "$pid"; then
            warning "Force killing backend process"
            kill -9 "$pid"
        fi
        
        rm -f "$BACKEND_PID_FILE"
        success "Backend stopped"
    else
        log "Backend is not running"
    fi
}

# Stop frontend service
stop_frontend() {
    local pid=$(get_pid "$FRONTEND_PID_FILE")
    
    if is_process_running "$pid"; then
        log "Stopping frontend service (PID: $pid)..."
        kill "$pid"
        
        # Wait for graceful shutdown
        local attempts=10
        while [[ $attempts -gt 0 ]] && is_process_running "$pid"; do
            sleep 1
            ((attempts--))
        done
        
        # Force kill if still running
        if is_process_running "$pid"; then
            warning "Force killing frontend process"
            kill -9 "$pid"
        fi
        
        rm -f "$FRONTEND_PID_FILE"
        success "Frontend stopped"
    else
        log "Frontend is not running"
    fi
}

# Stop all services
stop_services() {
    log "Stopping all services..."
    stop_backend
    stop_frontend
}

# Start all services
start_services() {
    log "Starting all services..."
    
    # Start backend first
    if start_backend; then
        # Start frontend
        if start_frontend; then
            success "All services started successfully!"
            log "Backend: http://localhost:$BACKEND_PORT"
            log "Frontend: http://localhost:$FRONTEND_PORT"
            log "API Docs: http://localhost:$BACKEND_PORT/docs"
        else
            error "Failed to start frontend"
            stop_backend
            return 1
        fi
    else
        error "Failed to start backend"
        return 1
    fi
}

# Restart all services
restart_services() {
    log "Restarting all services..."
    stop_services
    sleep 2
    start_services
}

# Show service status
show_status() {
    log "Service Status:"
    
    # Backend status
    local backend_pid=$(get_pid "$BACKEND_PID_FILE")
    if is_process_running "$backend_pid"; then
        if check_port $BACKEND_PORT; then
            success "Backend: Running (PID: $backend_pid, Port: $BACKEND_PORT)"
        else
            warning "Backend: Process running but port not accessible (PID: $backend_pid)"
        fi
    else
        error "Backend: Not running"
    fi
    
    # Frontend status
    local frontend_pid=$(get_pid "$FRONTEND_PID_FILE")
    if is_process_running "$frontend_pid"; then
        if check_port $FRONTEND_PORT; then
            success "Frontend: Running (PID: $frontend_pid, Port: $FRONTEND_PORT)"
        else
            warning "Frontend: Process running but port not accessible (PID: $frontend_pid)"
        fi
    else
        error "Frontend: Not running"
    fi
}

# Show logs
show_logs() {
    local service=${1:-"all"}
    
    case $service in
        "backend")
            if [[ -f "$LOG_DIR/backend.log" ]]; then
                tail -f "$LOG_DIR/backend.log"
            else
                error "Backend log file not found"
            fi
            ;;
        "frontend")
            if [[ -f "$LOG_DIR/frontend.log" ]]; then
                tail -f "$LOG_DIR/frontend.log"
            else
                error "Frontend log file not found"
            fi
            ;;
        "all"|*)
            log "Showing all logs (Ctrl+C to exit)..."
            if [[ -f "$LOG_DIR/backend.log" ]] && [[ -f "$LOG_DIR/frontend.log" ]]; then
                tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log"
            elif [[ -f "$LOG_DIR/backend.log" ]]; then
                tail -f "$LOG_DIR/backend.log"
            elif [[ -f "$LOG_DIR/frontend.log" ]]; then
                tail -f "$LOG_DIR/frontend.log"
            else
                error "No log files found"
            fi
            ;;
    esac
}

# Show help
show_help() {
    echo "NeoNova Service Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start           Start all services (backend + frontend)"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  status          Show service status"
    echo "  logs [service]  Show logs (all, backend, or frontend)"
    echo "  backend         Start only backend service"
    echo "  frontend        Start only frontend service"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start        # Start all services"
    echo "  $0 logs backend # Show backend logs"
    echo "  $0 status       # Check service status"
}

# Main script logic
main() {
    local command=${1:-"start"}
    
    case $command in
        "start")
            start_services
            # Keep script running to monitor services
            log "Services are running. Press Ctrl+C to stop all services."
            while true; do
                sleep 10
                # Check if services are still running
                local backend_pid=$(get_pid "$BACKEND_PID_FILE")
                local frontend_pid=$(get_pid "$FRONTEND_PID_FILE")
                
                if ! is_process_running "$backend_pid"; then
                    error "Backend process died unexpectedly"
                    break
                fi
                
                if ! is_process_running "$frontend_pid"; then
                    error "Frontend process died unexpectedly"
                    break
                fi
            done
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            restart_services
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs "$2"
            ;;
        "backend")
            start_backend
            ;;
        "frontend")
            start_frontend
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"