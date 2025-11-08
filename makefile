# Makefile

# Phony targets
.PHONY: setup install run

# Set the default goal to 'help' to list available commands
.DEFAULT_GOAL := help

# Dynamic Help Target
help:
	@echo "Available Make Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}' | \
		sort

setup: # Setting up virtual environment
	@echo "Setting up virtual environment..."
	python3 -m venv .venv
	@echo "✅ Environment is set up. Activate with: source .venv/bin/activate"

install: # Install dependencies
	@echo "Installing dependencies"
	pip install -r requirements.txt
	@echo "✅ Dependencies installed."

run: # Run apps
	@echo "Running app..."
	python3 -m examples.example1
	python3 -m examples.example2
