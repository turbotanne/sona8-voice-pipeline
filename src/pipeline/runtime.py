class PipelineRuntime:
    def run(self, steps):
        for step in steps:
            yield step