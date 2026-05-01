# Prompt Dashboard

The prompt dashboard provides a lightweight way to monitor hallucinations, token usage and latency across logged prompts.

## Data Format

Logs are expected as JSONL with the following keys per line:

```json
{
  "prompt_id": "string",
  "system_prompt": "string",
  "user_prompt": "string",
  "response": "string",
  "hallucination": false,
  "tokens": 123,
  "latency_ms": 250
}
```

## CLI Usage

```bash
python -m src.cli.prompt_dashboard logs/prompt_samples.jsonl --output reports/prompt-metrics.json --top 10
```

This prints key metrics to stdout and writes a JSON report if `--output` is provided.

## Integration Ideas

- Schedule the CLI via GitHub Actions / cron and publish metrics to Slack.
- Feed the JSON output into a Streamlit dashboard for richer visualizations.
- Extend the JSONL schema with `meeting_type` to filter results per template.
