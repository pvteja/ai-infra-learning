# AI Infrastructure Lab

My hands-on, 6-month path from senior data engineer to **AI infrastructure / AI platform engineer**, built on **Microsoft Azure**.

Each folder is one day of work: real code, real configs, and notes on what I learned and what broke along the way.

## About me

Senior Data Engineer with ~9 years of experience building data and AI platforms (Snowflake, dbt, Matillion, Cortex AI, agentic and RAG systems). This repo documents my move into AI infrastructure: containers, Kubernetes, model serving, GPUs, LLM gateways, and production AI platforms on Azure.

## Week 1: Containers (complete)

Built a FastAPI service backed by **Postgres** and a **Redis** cache, running together with **Docker Compose**, and shipped the image to **Azure Container Registry**.

| Day | Topic | Highlights |
|---|---|---|
| 1 | Containerize a FastAPI app | First Dockerfile, build, run, inspect |
| 2 | Images, layers, caching | Layer ordering so code changes don't reinstall dependencies |
| 3 | Smaller, safer images | Multi-stage build, `.dockerignore`, **non-root user** |
| 4 | Config and data | Env vars, `--env-file`, named volumes, bind mounts; fixed a non-root `/data` permission error |
| 5 | Docker Compose | API + Postgres, service-name networking, healthchecks, persistent volume |
| 6 | Azure Container Registry | Resource group, ACR, `az acr login`, version + Git-commit image tags, budget alert |
| 7 | Mini project | Redis cache-aside, invalidation + TTL, **fail-open** when Redis is down, scaled to 3 stateless replicas |

### Results

- **Caching:** `/notes` latency dropped from **~1,000 ms** (database) to **~3 ms** (Redis cache).
- **Image size:** switching from `python:3.12` to `python:3.12-slim` cut the image from **1.67 GB to 245 MB** (about 7× smaller).
- **Resilience:** with Redis stopped, the API keeps serving from Postgres instead of returning errors.
- **Scaling:** 3 API replicas share one visit counter, because all state lives in Redis and Postgres, not in the containers.

## Architecture (Day 7)

```
            ┌──────────────┐
 request ──▶│  FastAPI (×3) │── cache hit ──▶ Redis (cache, TTL 30s)
            └──────┬───────┘
                   │ cache miss
                   ▼
              Postgres (notes, persistent volume)
```

## Run it

Requires Docker Desktop.

```bash
cd day7
# create .env with POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, APP_NAME
docker compose up -d --build
```

Then open:
- http://localhost:8000/docs for the interactive API
- http://localhost:8000/health for the DB and cache status
- http://localhost:8000/notes to see `source: database` vs `source: cache`

Scale to 3 replicas:

```bash
docker compose up -d --scale api=3
```

## Tech stack

Python · FastAPI · Docker · Docker Compose · PostgreSQL · Redis · Azure Container Registry · Azure CLI

## Roadmap

| Month | Focus |
|---|---|
| 1 | Docker, Kubernetes, AKS, Helm, Key Vault |
| 2 | Terraform, Azure DevOps CI/CD, networking · **AI-103** |
| 3 | Microsoft Foundry, Azure OpenAI, API Management as an AI gateway |
| 4 | GPUs, vLLM and KAITO on AKS, cost benchmarking · **AZ-104** |
| 5 | RAG with Azure AI Search, agents, MCP, Forward Deployed Engineer programme |
| 6 | Observability, AI security, capstone AI platform · **CKA** |

## Repo layout

```
ai-infra-lab/
├── day4/   day5/   day7/   # each day's code and Dockerfile
├── notes/                  # day-by-day learning notes
└── README.md
```

---

Follow along as each week is added.