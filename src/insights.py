from statistics import mean

def engagement_delta(metrics):
    return mean(metrics) if metrics else 0.0