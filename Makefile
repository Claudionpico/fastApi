# Variables
VENV_PATH=venv/bin/activate       # Path to the virtual environment
PORT=8081                         # Port for the Uvicorn server
DIR ?=1-InitFastApi               # Default directory (can be changed when running make commands)

# Rules
.PHONY: activate run stop info

# 1. Activate the virtual environment in the specified directory
activate:
	bash -c "source $(DIR)/$(VENV_PATH)"

# 3. Run Uvicorn in the specified directory with automatic reload
run:
	uvicorn $(DIR).main:app --reload --port $(PORT)

# 4. Display information about Makefile usage
info:
	@echo "Makefile Usage:"
	@echo "make activate DIR=<directory>  - Activates the virtual environment in the specified directory."
	@echo "make run DIR=<directory>       - Runs Uvicorn in the specified directory on port $(PORT)."
	@echo "make info                      - Shows this help information."
	@echo "Current settings:"
	@echo "  Virtual environment path: $(VENV_PATH)"
	@echo "  Port: $(PORT)"
	@echo "  Default directory: $(DIR)"
