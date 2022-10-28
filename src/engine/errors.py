from fastapi import HTTPException


class ImproperRequirementError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400)


class UnloadedPluginError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=405)


class MissingPackageInput(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400)
