import pytest

from src.pipeline.runtime import PipelineRuntime


def test_unknown_step_raises():
    runtime = PipelineRuntime(registry={})
    with pytest.raises(ValueError):
        runtime.run(["does-not-exist"], {"text": "hello"})


def test_run_job_returns_summary():
    runtime = PipelineRuntime()
    result = runtime.run_job("hello world from sona8")
    assert result["summary"].startswith("hello")
    assert "executed_steps" in result["metadata"]
