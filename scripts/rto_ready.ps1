docker compose --profile dev restart web_dev | Out-Null
$start = Get-Date
do {
  Start-Sleep -Milliseconds 200
  try { Invoke-WebRequest -UseBasicParsing http://localhost:8000/ready | Out-Null; $ok = $true }
  catch { $ok = $false }
} until ($ok)
$elapsed = (Get-Date - $start).TotalMilliseconds
"rto_ready_ms=$([math]::Round($elapsed,1))"
