# fastapi_project

A first FastAPI project using a small MVC-style architecture.

## Architecture

- `models/` contains Pydantic models and validation rules.
- `controllers/` contains application behavior and PostgreSQL persistence.
- `database.py` manages PostgreSQL connections and initializes the items table.
- `main.py` contains the FastAPI routes and delegates requests to controllers.

## Run locally

Activate the virtual environment and start the development server:

```bash
source .venv/bin/activate
python main.py
```

Open the interactive API documentation at http://127.0.0.1:8000/docs.
Every request is also printed in the terminal, for example: `[API] GET /items -> 200`.

## Run the API client

Keep the API server running in one terminal. In a second terminal, run:

```bash
uv run entrypoint.py
```

The client performs a `GET /items`, a `POST /items`, and another `GET /items`.
If `uv` is not installed, use the project environment directly:

```bash
.venv/bin/python entrypoint.py
```

## Endpoints

- `GET /` returns a welcome message.
- `GET /health` returns the service status.
- `GET /items` returns all created items.
- `POST /items` validates and creates an item with `name`, `description`, and `price` fields.

Items are stored in PostgreSQL and survive API restarts.

## Run with Docker

Build and start the API container:

```bash
docker build -t fastapi-project .
docker run --rm -p 8000:8000 fastapi-project
```

Open http://127.0.0.1:8000/docs to view and call the API.

## Run API and PostgreSQL with containers

The project includes a PostgreSQL service in `compose.yaml`. The API can reach
the database at `db:5432` inside the container network. The database data is
stored in the named `postgres_data` volume, so it survives container restarts.

If Docker Compose is available, start both containers with:

```bash
docker compose up --build
```

The API is available at http://127.0.0.1:8000 and PostgreSQL is available at
`127.0.0.1:5432` from the host. Stop the services with:

```bash
docker compose down
```

The API uses the PostgreSQL database container for item persistence.

If your Docker installation does not include Compose, start the database as a
second container with the Docker CLI:

```bash
docker network create fastapi-network
docker run -d --name fastapi-db \
	--network fastapi-network \
	-e POSTGRES_DB=app_db \
	-e POSTGRES_USER=app_user \
	-e POSTGRES_PASSWORD=app_password \
	-p 5432:5432 \
	-v postgres_data:/var/lib/postgresql/data \
	postgres:16-alpine
```

Stop and remove that database container with:

```bash
docker stop fastapi-db
docker rm fastapi-db
```
