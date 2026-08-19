# Flask Calculator - Frontend + Backend Containers

A simple calculator application with:
- Frontend: Flask + HTML/CSS/JavaScript
- Backend: Flask REST API
- Two separate Docker images
- Docker Compose for local testing

## Architecture

Browser
  |
  | HTTP :8000
  v
Frontend Flask container
  |
  | POST /calculate :5000
  v
Backend Flask container

## Run with Docker Compose

```bash
docker compose up --build
```

Open:

http://localhost:8000

Backend health check:

http://localhost:5000/health

## Build images separately

```bash
docker build -t calculator-backend:1.0 ./backend
docker build -t calculator-frontend:1.0 ./frontend
```

## Run containers separately

Backend:

```bash
docker run -d --name calculator-backend -p 5000:5000 calculator-backend:1.0
```

Frontend:

```bash
docker run -d --name calculator-frontend -p 8000:8000   -e BACKEND_URL=http://localhost:5000   calculator-frontend:1.0
```

Open:

http://localhost:8000

## API

POST `/calculate`

Request:

```json
{
  "num1": 10,
  "num2": 5,
  "operation": "add"
}
```

Supported operations:

- add
- subtract
- multiply
- divide

Example response:

```json
{
  "result": 15
}
```
