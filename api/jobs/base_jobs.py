class Job:
    def queue(self) -> None:
        """Put's the current task onto the configured queue for processing asynchronously"""
        pass

    def before_start(self) -> None:
        """Hook method called before calling the handle method for processing"""
        pass
