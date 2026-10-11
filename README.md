# Flask + PostgreSQL DevOps Demo App

A containerized Flask application with PostgreSQL, built as a hands-on DevOps project to practice Docker, Docker Compose, database integration, health checks, and Prometheus monitoring.

## Architecture

```text
                 Client / Browser
                        |
                    Port 5000
                        |
                   Flask App
                    /      \
             REST API     /metrics
                |            |
                v            v
           PostgreSQL    Prometheus
                |
         Docker Volume
        (Persistent Data)
```

The Flask application and PostgreSQL database communicate through a dedicated Docker Compose network.

## Tech Stack

- **Python 3.14** — Application runtime
- **Flask 3.1** — Web framework
- **PostgreSQL 17** — Relational database
- **Docker** — Containerization
- **Docker Compose** — Multi-container deployment
- **Prometheus Flask Exporter** — Application metrics
- **psycopg2** — PostgreSQL connection

## Features

- Containerized Flask application
- PostgreSQL integration
- REST endpoints for application health and database records
- PostgreSQL readiness check using `pg_isready`
- Automatic database initialization through `init.sql`
- Persistent PostgreSQL data using a named Docker volume
- Service startup dependency based on database health
- Prometheus HTTP metrics exposed at `/metrics`
- Environment-based configuration

## Project Structure

```text
demo-app/
├── app.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── init.sql
├── .env.example
├── .dockerignore
├── .gitignore
└── README.md
```

## Prerequisites

- Docker Engine
- Docker Compose v2

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/vec1or/demo-app.git
cd demo-app
```

**2. Configure environment variables**

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` and set your local PostgreSQL password. Do not commit `.env` to Git.

**3. Build and start the application**

```bash
docker compose up -d --build
```

**4. Check container status**

```bash
docker compose ps
```

**5. Test the application**

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/messages
curl http://localhost:5000/metrics
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns a welcome message |
| GET | `/health` | Checks PostgreSQL connectivity |
| GET | `/messages` | Returns records from the messages table |
| GET | `/metrics` | Exposes Prometheus application metrics |

### Example health response

```json
{
  "status": "ok",
  "environment": "development",
  "database": "up"
}
```

When PostgreSQL is unavailable, `/health` returns HTTP 503.

## PostgreSQL Persistence

The database uses the named Docker volume `demo-db-data` for persistent storage.

On the first database initialization, PostgreSQL executes `init.sql` to create the `messages` table and insert a demonstration record.

Initialization scripts are not automatically rerun when an existing database volume is reused.

## Monitoring

The application uses `prometheus_flask_exporter` to expose HTTP request metrics.

Useful PromQL queries include:

```promql
sum(rate(flask_http_request_total[5m]))
```

```promql
sum(rate(flask_http_request_duration_seconds_sum[5m]))
/
sum(rate(flask_http_request_duration_seconds_count[5m]))
```

For a full Prometheus, Grafana, Loki, Alloy, and Alertmanager environment, see the companion project:

[DevOps Monitoring Stack](https://github.com/vec1or/devops-monitoring-stack)

## Troubleshooting

**Check application logs**

```bash
docker compose logs app --tail=50
```

**Check PostgreSQL logs**

```bash
docker compose logs db --tail=50
```

**Check database readiness**

```bash
docker compose exec db pg_isready -U devops -d demoapp
```

**Rebuild the application**

```bash
docker compose up -d --build app
```

## Stopping the Application

Stop and remove containers:

```bash
docker compose down
```

This preserves the named database volume.

To also delete the volume:

```bash
docker compose down -v
```

**Warning:** The second command permanently deletes database data stored in the Compose-managed volume.

## Security Considerations

This project is intended for local development and educational use.

For production deployments, consider using a production WSGI server, stronger secrets management, restricted network exposure, automated tests, and secure database credentials.

## Related Projects

- [Terraform Docker Infrastructure](https://github.com/vec1or/terraform-docker-infrastructure)
- [DevOps Monitoring Stack](https://github.com/vec1or/devops-monitoring-stack)
- [Ansible Ubuntu Automation](https://github.com/vec1or/ansible-ubuntu-automation)
