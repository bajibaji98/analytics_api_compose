# Analytics API (FastAPI + Postgres, Docker Compose)

Portable, laptop-first setup with clear health/readiness checks and safe env handling.

## Quick Start (Dev)
```powershell
Copy-Item .env.example .env
docker compose --profile dev up -d --build
Invoke-WebRequest http://localhost:8000/health  | Out-Null
Invoke-WebRequest http://localhost:8000/ready   | Out-Null
```

App: http://localhost:8000/  
Health: `GET /health` (fast)  
Readiness: `GET /ready` (DB ping)

## Prod-like (no host port)
```powershell
docker compose --profile prod up -d --build
# use docker exec or an internal client to reach web
```

## Evidence Commands
```powershell
docker images | findstr /I "analytics python postgres"
powershell -File .\scripts\time_to_healthy.ps1
powershell -File .\scripts\burst_p95.ps1
docker stats --no-stream
powershell -File .\scripts\rto_ready.ps1
```

## Troubleshooting
- Port 8000 busy → change `web_dev.ports` in compose.
- `/ready` 503 → check DB logs: `docker compose logs pg`.
- Windows shell quirks → use the PowerShell scripts in `scripts/`.
