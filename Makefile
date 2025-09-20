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
	@echo "  local      - Run Flask locally with PostgreSQL in Docker"
	@echo "  local-down - Stop PostgreSQL container"

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

# Local development with Docker PostgreSQL
local:
	@echo "Creating .env file for local development..."
	@echo "DB_HOST=localhost" > .env
	@echo "DB_NAME=todoapp" >> .env
	@echo "DB_USER=postgres" >> .env
	@echo "DB_PASSWORD=password" >> .env
	@echo "DB_PORT=5432" >> .env
	@echo "FLASK_DEBUG=True" >> .env
	@echo "FLASK_ENV=development" >> .env
	@echo "PORT=5001" >> .env
	@echo "Starting PostgreSQL with Docker Compose..."
	@docker-compose up -d db
	@echo "Waiting for database to be ready..."
	@sleep 5
	@echo "Initializing database schema..."
	@python -c "from functions.models import Schema; Schema()"
	@echo "Starting Flask application locally..."
	@echo "Application will be available at http://localhost:5001"
	@python app.py

# Stop local development
local-down:
	@echo "Stopping PostgreSQL container..."
	@docker-compose stop db

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
