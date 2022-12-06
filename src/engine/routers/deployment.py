from typing import Any, Dict

from fastapi import APIRouter

from ..engine import PluginEngine
from ..errors import *
from ..schemas.payloads import StarpackInput

router = APIRouter()


@router.post("/deploy")
async def deploy(starpack_input: StarpackInput):
    engine = PluginEngine()

    if starpack_input.deployment is None:
        raise MissingInputError("deployment")

    datastore: Dict[str, Any] = dict()

    # Add metadata about packaging if we have it
    if starpack_input.package:
        datastore["package_metadata"] = starpack_input.package.metadata

    deployment_input = starpack_input.deployment
    datastore["metadata"] = deployment_input.metadata

    for step in deployment_input.steps:
        print(f"Running {step.name}")
        datastore["step_data"] = step.dict()
        engine.invoke(step.name, datastore)
        datastore.pop("step_data")

    # If we have it, return the endpoint. Otherwise, just give it a null value.
    return {"endpoint": datastore.get("endpoint")}
