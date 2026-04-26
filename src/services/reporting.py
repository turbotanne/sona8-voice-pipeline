class ReportingService:
    def render(self, metrics):
        return {"rows": len(metrics)}