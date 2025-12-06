class BlueprintError(Exception):
    pass


class ValidationError(BlueprintError):
    def __init__(self, message: str, rule: str | None = None):
        prefix = f"[{rule}] " if rule else ""
        super().__init__(f"{prefix}{message}")
        self.rule = rule


class DependencyError(ValidationError):
    pass


class SlotError(ValidationError):
    pass

