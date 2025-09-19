# Makefile for Flask Todo Application

.PHONY: help build up down logs shell db-shell clean install test

# Default target
help:
	@echo "Available commands:"
	@echo "  build      - Build Docker images"
	@echo "  up         - Start the application with Docker Compose"
	@echo "  down       - Stop the application"
	@echo "  logs       - Show application logs"
	@echo "  shell      - Open shell in Flask container"
	@echo "  db-shell   - Open PostgreSQL shell"
	@echo "  clean      - Clean up containers and volumes"
	@echo "  install    - Install dependencies locally"
	@echo "  test       - Run tests"
	@echo "  dev        - Run in development mode (local)"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web bash

db-shell:
	docker-compose exec db psql -U postgres -d todoapp

# Development commands
install:
	pip install -r requirements.txt

dev:
	@echo "Make sure PostgreSQL is running locally on port 5432"
	@echo "Database: todoapp, User: postgres, Password: password"
	python app.py

# Cleanup
clean:
	docker-compose down -v
	docker system prune -f

# Test commands
test:
	docker-compose exec web python -m pytest

# Database initialization
init-db:
	docker-compose exec web python -c "from functions.models import Schema; Schema()"

# Full setup
setup: build up
	@echo "Waiting for services to be ready..."
	@sleep 10
	@make init-db
	@echo "Application is ready at http://localhost:5000"
