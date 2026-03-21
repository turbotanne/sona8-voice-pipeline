param(
  [string]$Tag = "latest"
)
Set-StrictMode -Version Latest
az acr login --name sona8
az acr repository show-tags --name sona8 --repository voice-pipeline | Out-Null