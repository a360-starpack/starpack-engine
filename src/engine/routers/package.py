from typing import Any, Dict
from fastapi import APIRouter

from ..engine import PluginEngine

from ..schemas.payloads import StarpackInput
from ..errors import *

router = APIRouter()


@router.post("/package")
async def package(starpack_input: StarpackInput):
    """
    Takes in a payload dictionary of packaging steps to create a deployment.
    """
    if starpack_input.package is None:
        raise MissingInputError("package")

    # Create a plugin engine instance
    engine = PluginEngine()

    datastore: Dict[str, Any] = dict()

    package_input = starpack_input.package
    datastore["artifacts"] = package_input.artifacts
    datastore["metadata"] = package_input.metadata

    for step in package_input.steps:
        print(f"Running {step.name}")
        datastore["step_data"] = step.dict()
        engine.invoke(step.name, datastore)
        datastore.pop("step_data")

    return {"status": "You did it!"}
