#!/bin/bash

# Flet Calculator App - Test Runner Script
# This script automatically activates the virtual environment and runs tests

set -euo pipefail  # Exit on error, unset vars, or pipe failure

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
PYTHON_VENV="$VENV_PATH/bin/python"
PYTEST_BIN="$VENV_PATH/bin/pytest"
TEST_DIR="$PROJECT_ROOT/tests"

echo -e "${BLUE}🧪 Flet Calculator - Test Runner${NC}"
echo "Project root: $PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}❌ Virtual environment not found at: $VENV_PATH${NC}"
    echo -e "${YELLOW}💡 Please run 'make venv' first to create the virtual environment${NC}"
    exit 1
fi

# Check if tests directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}❌ Tests directory not found at: $TEST_DIR${NC}"
    echo -e "${YELLOW}💡 Please create tests/ directory and implement tests${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}🐍 Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Verify pytest is installed
if [ ! -f "$PYTEST_BIN" ]; then
    echo -e "${YELLOW}📦 pytest not found, installing...${NC}"
    pip install pytest
fi

# Verify test files exist
if [ ! -f "$TEST_DIR/test_logic.py" ]; then
    echo -e "${YELLOW}⚠️  test_logic.py not found in tests/ directory${NC}"
    echo -e "${YELLOW}💡 Please implement tests/test_logic.py${NC}"
fi

echo -e "${GREEN}🧪 Running tests...${NC}"
echo ""

# Change to project directory
cd "$PROJECT_ROOT"

# Set Python path to include project root
export PYTHONPATH="$PROJECT_ROOT:${PYTHONPATH:-}"

# Default pytest arguments
PYTEST_ARGS=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            PYTEST_ARGS="$PYTEST_ARGS -v"
            echo -e "${YELLOW}📝 Verbose mode enabled${NC}"
            shift
            ;;
        -q|--quiet)
            PYTEST_ARGS="$PYTEST_ARGS -q"
            echo -e "${YELLOW}🔇 Quiet mode enabled${NC}"
            shift
            ;;
        -s|--no-capture)
            PYTEST_ARGS="$PYTEST_ARGS -s"
            echo -e "${YELLOW}📤 Output capture disabled${NC}"
            shift
            ;;
        --coverage)
            if command -v coverage &> /dev/null; then
                echo -e "${YELLOW}📊 Coverage mode enabled${NC}"
                coverage run -m pytest $PYTEST_ARGS tests/
                echo ""
                echo -e "${BLUE}📈 Coverage Report:${NC}"
                coverage report -m
                exit 0
            else
                echo -e "${YELLOW}⚠️  coverage not installed, running tests without coverage${NC}"
            fi
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -v, --verbose     Verbose output"
            echo "  -q, --quiet       Quiet output"
            echo "  -s, --no-capture  Don't capture output"
            echo "  --coverage        Run with coverage (requires coverage package)"
            echo "  --help            Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                # Run all tests"
            echo "  $0 -v             # Run with verbose output"
            echo "  $0 -q             # Run with minimal output"
            echo "  $0 --coverage     # Run with coverage report"
            exit 0
            ;;
        *)
            # Pass unknown arguments to pytest
            PYTEST_ARGS="$PYTEST_ARGS $1"
            shift
            ;;
    esac
done

# Run pytest with collected arguments
echo -e "${GREEN}🏃 Executing: pytest $PYTEST_ARGS tests/${NC}"
$PYTEST_BIN $PYTEST_ARGS tests/

# Check test result
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed successfully!${NC}"
    echo -e "${GREEN}🎉 Calculator logic is working correctly${NC}"
else
    echo -e "${RED}❌ Some tests failed (exit code: $TEST_EXIT_CODE)${NC}"
    echo -e "${YELLOW}💡 Please check the test output above and fix any issues${NC}"
fi

exit $TEST_EXIT_CODE
