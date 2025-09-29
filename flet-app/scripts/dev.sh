#!/bin/bash

# Flet Calculator App - Development Server Startup Script
# This script automatically activates the virtual environment and starts the app

set -euo pipefail  # Exit on error, unset vars, or pipe failure

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
PYTHON_VENV="$VENV_PATH/bin/python"
MAIN_MODULE="$PROJECT_ROOT/main.py"

echo -e "${GREEN}🧮 Flet Calculator - Development Server${NC}"
echo "Project root: $PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}❌ Virtual environment not found at: $VENV_PATH${NC}"
    echo -e "${YELLOW}💡 Please run 'make venv' first to create the virtual environment${NC}"
    exit 1
fi

# Check if main.py exists
if [ ! -f "$MAIN_MODULE" ]; then
    echo -e "${RED}❌ Main module not found at: $MAIN_MODULE${NC}"
    echo -e "${YELLOW}💡 Please implement main.py first${NC}"
    exit 1
fi

# Activate virtual environment and check Python
echo -e "${GREEN}🐍 Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Verify flet (all extras) is installed
if ! $PYTHON_VENV - <<'PY'
import importlib.util

spec = importlib.util.find_spec("flet")
raise SystemExit(0 if spec else 1)
PY
then
    echo -e "${RED}❌ Flet is not installed in the virtual environment${NC}"
    echo -e "${YELLOW}💡 Installing flet[all]...${NC}"
    pip install 'flet[all]'
fi

echo -e "${GREEN}🚀 Starting Flet development server...${NC}"
echo -e "${YELLOW}📱 The app will be available at: http://localhost:8550${NC}"
echo -e "${YELLOW}⏹️  Press Ctrl+C to stop the server${NC}"
echo ""

# Change to project directory and run the app
cd "$PROJECT_ROOT"

# Run the application with environment variables for development
export FLET_WEB_APP_PORT=8550
export FLET_WEB_APP_HOST="0.0.0.0"

# Start the app
$PYTHON_VENV "$MAIN_MODULE" "$@"
