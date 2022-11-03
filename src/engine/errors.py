from fastapi import HTTPException


class ImproperRequirementError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400)


class UnloadedPluginError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=405)


class MissingInputError(HTTPException):
    def __init__(self, input_type: str) -> None:
        super().__init__(
            status_code=400, detail=f"Missing the following input type: {input_type}"
        )
