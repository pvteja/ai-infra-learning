# Day 5: Docker Compose with FastAPI and Postgres

## What I built
- FastAPI app with a `/notes` API backed by Postgres, both running with one command: `docker compose up -d --build`
- `/health` endpoint that checks the database connection, not just the app

## Key concepts
- **Docker Compose**: Describes multiple containers, their settings, networks and volumes in one `docker-compose.yml` file instead of long `docker run` commands.
- **Service names as hostnames**: Containers in the same Compose project reach each other by service name (`@db:5432`), because Compose creates a private network with built-in DNS.
- **`localhost` inside a container**: Means the container itself, not my laptop or other containers. To reach another service, use its name.
- **`depends_on` with healthcheck**: `condition: service_healthy` makes the API wait until Postgres passes `pg_isready`, so the API doesn't crash with "connection refused" on startup.
- **`pgdata` volume**: Named volume mounted at `/var/lib/postgresql/data`, so database data survives container restarts.
- **`.env` substitution**: Compose automatically reads `.env` and fills in `${POSTGRES_USER}`-style values in the YAML.
- **`$$` in healthcheck**: Escapes `$` so Compose doesn't replace the variable; the container's shell reads it instead.
- **Parameterized SQL (`%s`)**: Passes values safely to Postgres and prevents SQL injection.

## down vs down -v
- `docker compose down`: removes containers and network, **keeps volumes**, so data survives.
- `docker compose down -v`: also **deletes volumes**, so all data is gone. Never use it on data I care about.

## What I observed
- `socket.gethostbyname('db')` from the API container returned an internal IP like 172.18.0.x.
- Notes survived `down` + `up`, and were wiped after `down -v`.
- Checked data directly with `docker compose exec db psql -U app -d appdb -c "SELECT * FROM notes;"`

## Gotchas
- Postgres only reads `POSTGRES_*` variables on the **first** start. Changing the password in `.env` later causes "password authentication failed" until the volume is reset.
- `.env` must stay in `.gitignore`.

## Handy commands
- `docker compose ps`: status of all services
- `docker compose logs -f api`: follow logs for one service
- `docker compose exec <service> <cmd>`: run a command in a service
- `docker compose restart api`: restart one service
- `docker compose up -d --build`: rebuild and restart after code changes

## Kubernetes link
- Compose service names → Kubernetes **Services** (Day 10)
- Healthcheck → **liveness/readiness probes** (Day 17)
- Named volume → **PersistentVolume** on AKS

## Next
Day 6: push the image to Azure Container Registry.