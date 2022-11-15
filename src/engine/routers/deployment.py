from typing import Any, Dict
from fastapi import APIRouter

from ..plugengine.engine import PluginEngine

from ..schemas.payloads import StarpackInput
from ..errors import *

router = APIRouter()


@router.post("/deploy")
async def deploy(starpack_input: StarpackInput):
    engine = PluginEngine()

    if starpack_input.deployment is None:
        raise MissingInputError("deployment")

    datastore: Dict[str, Any] = dict()

    deployment_input = starpack_input.deployment
    datastore["metadata"] = deployment_input.metadata

    for step in deployment_input.steps:
        print(f"Running {step.name}")
        datastore["step_data"] = step.dict()
        engine.invoke(step.name, datastore)
        datastore.pop("step_data")

    return {"status": "You did it!"}
