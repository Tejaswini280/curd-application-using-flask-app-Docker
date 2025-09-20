# Flask Todo Application

A simple todo application built with Flask and PostgreSQL, containerized with Docker.

## Features

- Add, edit, and delete todo items
- PostgreSQL database backend
- Docker containerization
- Bootstrap UI
- RESTful API endpoints

## Quick Start with Docker

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd 16_Todo_appliation_in_flask
   ```

2. **Start the application:**
   ```bash
   make setup
   ```
   This will build the images, start the services, initialize the database, and make the app available at http://localhost:5000

3. **Or manually:**
   ```bash
   docker-compose up -d
   ```

## Available Commands

Use the Makefile for common operations:

```bash
make help          # Show all available commands
make build         # Build Docker images
make up            # Start the application
make down          # Stop the application
make logs          # Show application logs
make shell         # Open shell in Flask container
make db-shell      # Open PostgreSQL shell
make clean         # Clean up containers and volumes
make dev           # Run in development mode (local)
```

## Development

### Local Development (without Docker)

1. **Install PostgreSQL** locally
2. **Create database:**
   ```sql
   CREATE DATABASE todoapp;
   ```
3. **Set environment variables:**
   ```bash
   export DB_HOST=localhost
   export DB_NAME=todoapp
   export DB_USER=postgres
   export DB_PASSWORD=your_password
   export DB_PORT=5432
   ```
4. **Install dependencies:**
   ```bash
   make install
   ```
5. **Run the application:**
   ```bash
   make dev
   ```

### Environment Variables

- `DB_HOST`: Database host (default: localhost)
- `DB_NAME`: Database name (default: todoapp)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password (default: password)
- `DB_PORT`: Database port (default: 5432)
- `FLASK_DEBUG`: Enable debug mode (default: False)
- `PORT`: Application port (default: 5000)

## API Endpoints

- `GET /` - Main todo list page
- `GET /hey` - Health check endpoint
- `POST /insert` - Add new todo
- `GET /delete?id=<id>` - Delete todo
- `GET /query_edit?id=<id>` - Edit todo form
- `POST /edit` - Update todo

## Database Schema

```sql
CREATE TABLE "Todo" (
  "id" SERIAL PRIMARY KEY,
  "Title" TEXT,
  "Description" TEXT,
  "_is_deleted" BOOLEAN DEFAULT FALSE,
  "CreatedOn" DATE DEFAULT CURRENT_DATE,
  "DueDate" DATE
);
```

## Docker Services

- **web**: Flask application (port 5000)
- **db**: PostgreSQL database (port 5432)

## Troubleshooting

1. **Port conflicts**: If port 5000 is in use, change the port in docker-compose.yml
2. **Database connection**: Ensure PostgreSQL is running and accessible
3. **Permissions**: Make sure Docker has proper permissions to access the project directory

## License

MIT License
