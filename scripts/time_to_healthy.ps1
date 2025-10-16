$start = Get-Date
docker compose --profile dev up -d --build | Out-Null
do {
  Start-Sleep -Milliseconds 200
  try { Invoke-WebRequest -UseBasicParsing http://localhost:8000/health | Out-Null; $ok = $true }
  catch { $ok = $false }
} until ($ok)
$elapsed = (Get-Date - $start).TotalMilliseconds
"time_to_healthy_ms=$([math]::Round($elapsed,1))"
