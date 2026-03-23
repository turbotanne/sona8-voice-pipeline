param(
  [string]$Bucket = "sona8-data"
)
aws s3 sync data/ s3://$Bucket/data/