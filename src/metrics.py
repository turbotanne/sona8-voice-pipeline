def compute_latency(jobs):
    return sum(jobs) / max(len(jobs), 1)