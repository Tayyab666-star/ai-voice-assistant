# AI Voice Assistant Makefile

.PHONY: help build up down logs test clean install

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

test: ## Run all tests
	python tests/test_runner.py --suite all

test-unit: ## Run unit tests only
	python tests/test_runner.py --suite unit

test-integration: ## Run integration tests only
	python tests/test_runner.py --suite integration

test-performance: ## Run performance tests only
	python tests/test_runner.py --suite performance

test-bilingual: ## Run bilingual tests only
	python tests/test_runner.py --suite bilingual

test-e2e: ## Run end-to-end tests only
	python tests/test_runner.py --suite e2e

test-coverage: ## Generate code coverage report
	python tests/test_runner.py --coverage

test-service: ## Run tests for specific service (usage: make test-service SERVICE=call_handler)
	python tests/test_runner.py --service $(SERVICE)

test-clean: ## Clean test artifacts
	del /Q test-results*.xml test-report*.json coverage.xml .coverage 2>nul || echo "Cleaned test files"
	rmdir /S /Q htmlcov .pytest_cache 2>nul || echo "Cleaned test directories"

clean: ## Clean up Docker containers and images
	docker-compose down -v
	docker system prune -f

dev-call-handler: ## Run call handler service in development mode
	cd call_handler && python -m uvicorn main:app --reload --port 8000

dev-stt: ## Run STT service in development mode
	cd stt_service && python -m uvicorn main:app --reload --port 8001

dev-tts: ## Run TTS service in development mode
	cd tts_service && python -m uvicorn main:app --reload --port 8002

dev-nlu: ## Run NLU service in development mode
	cd nlu_service && python -m uvicorn main:app --reload --port 8003

dev-appointment: ## Run appointment service in development mode
	cd appointment_service && python -m uvicorn main:app --reload --port 8004

dev-sms: ## Run SMS service in development mode
	cd sms_service && python -m uvicorn main:app --reload --port 8005