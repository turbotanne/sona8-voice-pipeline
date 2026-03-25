param(
  [string]$Output = "metrics.csv"
)
Invoke-WebRequest -Uri "https://api.sona8.com/metrics" -OutFile $Output