# Flet Calculator App - Makefile

# Python settings
PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

# Application settings
APP_MODULE := main
TEST_DIR := tests

# Default target
.DEFAULT_GOAL := help

## Create virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing base dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install 'flet[all]' pytest
	@echo "Generating requirements.txt..."
	$(PIP) freeze > requirements.txt
	@echo "✅ Virtual environment created successfully!"
	@echo "📝 Activate with: source $(VENV_BIN)/activate"

## Install dependencies from requirements.txt
install:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed!"

## Start development server
dev:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@echo "Starting development server..."
	@./scripts/dev.sh

## Run the application (same as dev for now)
run: dev

## Run tests
test:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@echo "Running tests..."
	@./scripts/test.sh

## Run tests with verbose output
test-verbose:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@echo "Running tests (verbose)..."
	@./scripts/test.sh -v

## Run quick tests (minimal output)
test-quick:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@echo "Running tests (quick)..."
	@./scripts/test.sh -q

## Lint code (if linter is available)
lint:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@if $(PIP) show flake8 >/dev/null 2>&1; then \
		echo "Running flake8..."; \
		$(VENV_BIN)/flake8 app/ $(APP_MODULE).py; \
	else \
		echo "ℹ️  flake8 not installed. Install with: $(PIP) install flake8"; \
	fi

## Format code (if formatter is available)
format:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@if $(PIP) show black >/dev/null 2>&1; then \
		echo "Running black..."; \
		$(VENV_BIN)/black app/ $(APP_MODULE).py tests/; \
	else \
		echo "ℹ️  black not installed. Install with: $(PIP) install black"; \
	fi

## Clean up generated files
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true
	@echo "✅ Cleanup completed!"

## Remove virtual environment
clean-venv:
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "✅ Virtual environment removed!"

## Full cleanup (clean + clean-venv)
clean-all: clean clean-venv
	@echo "✅ Full cleanup completed!"

## Update dependencies
update:
	@if [ ! -d "$(VENV)" ]; then echo "❌ Virtual environment not found. Run 'make venv' first."; exit 1; fi
	@echo "Updating dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade 'flet[all]' pytest
	$(PIP) freeze > requirements.txt
	@echo "✅ Dependencies updated!"

## Check virtual environment status
status:
	@echo "📊 Project Status:"
	@if [ -d "$(VENV)" ]; then \
		echo "✅ Virtual environment: Active"; \
		echo "🐍 Python version: $$($(PYTHON_VENV) --version)"; \
		echo "📦 Installed packages:"; \
		$(PIP) list --format=columns | head -n 10; \
		if [ $$($(PIP) list | wc -l) -gt 11 ]; then echo "   ... and more"; fi; \
	else \
		echo "❌ Virtual environment: Not found"; \
		echo "💡 Run 'make venv' to create it"; \
	fi
	@echo ""
	@if [ -f "requirements.txt" ]; then \
		echo "📄 requirements.txt: Present"; \
	else \
		echo "❌ requirements.txt: Missing"; \
	fi

## Setup project for first time
setup: venv
	@echo "🚀 Setting up project for first time..."
	@chmod +x scripts/*.sh 2>/dev/null || echo "⚠️  No scripts to make executable"
	@echo "✅ Project setup completed!"
	@echo ""
	@echo "📋 Next steps:"
	@echo "   1. Run 'make test' to verify everything works"
	@echo "   2. Run 'make dev' to start development server"
	@echo "   3. Open browser and test the calculator"

## Show help
help:
	@echo "🧮 Flet Calculator App - Available Commands:"
	@echo ""
	@echo "🏗️  Setup & Environment:"
	@echo "   make venv         Create virtual environment"
	@echo "   make install      Install dependencies from requirements.txt"
	@echo "   make setup        First-time project setup (venv + permissions)"
	@echo "   make status       Show project status"
	@echo ""
	@echo "🚀 Development:"
	@echo "   make dev          Start development server"
	@echo "   make run          Run the application (alias for dev)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "   make test         Run all tests"
	@echo "   make test-verbose Run tests with verbose output"
	@echo "   make test-quick   Run tests with minimal output (-q)"
	@echo ""
	@echo "🔧 Code Quality:"
	@echo "   make lint         Run code linter (flake8)"
	@echo "   make format       Format code (black)"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "   make clean        Remove cache files and temp data"
	@echo "   make clean-venv   Remove virtual environment"
	@echo "   make clean-all    Full cleanup (clean + clean-venv)"
	@echo ""
	@echo "📦 Maintenance:"
	@echo "   make update       Update dependencies"
	@echo "   make help         Show this help message"
	@echo ""
	@echo "💡 Quick start: make setup && make dev"

.PHONY: venv install dev run test test-verbose test-quick lint format clean clean-venv clean-all update status setup help
