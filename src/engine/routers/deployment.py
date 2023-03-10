from typing import Any, Dict, Optional

from fastapi import APIRouter

from ..engine import PluginEngine
from ..errors import *
from ..schemas.payloads import StarpackInput

router = APIRouter()


@router.post("/deployment")
async def create_deployment(starpack_input: StarpackInput):
    engine = PluginEngine()

    if starpack_input.deployment is None:
        raise MissingInputError("deployment")

    datastore: Dict[str, Any] = dict()

    # Add metadata about packaging if we have it
    if starpack_input.package:
        datastore["package_metadata"] = starpack_input.package.metadata

    deployment_input = starpack_input.deployment
    datastore["metadata"] = deployment_input.metadata
    datastore["images"] = dict()

    for step in deployment_input.steps:
        print(f"Running {step.name}")
        datastore["step_data"] = step.dict()
        engine.invoke(step.name, datastore)
        datastore.pop("step_data")

    # If we have it, return the endpoint. Otherwise, just give it a null value.
    return {"endpoints": datastore.get("endpoints")}


@router.get("/deployment")
def get_deployments(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
):
    engine = PluginEngine()

    output = engine.invoke(
        plugin="docker_manage_deployments",
        input_data={"name": name, "version": version, "wrapper": wrapper},
        method="list",
    )

    if not output:
        raise HTTPException(
            404, detail="Unable to find any deployments matching the given parameters."
        )

    return output


@router.delete("/deployment")
def delete_deployments(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
):
    engine = PluginEngine()

    output = engine.invoke(
        plugin="docker_manage_deployments",
        input_data={"name": name, "version": version, "wrapper": wrapper},
        method="delete",
    )

    return output


@router.get("/logs")
def get_deployments(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
):
    engine = PluginEngine()

    output = engine.invoke(
        plugin="docker_manage_deployments",
        input_data={"name": name, "version": version, "wrapper": wrapper},
        method="logs",
    )

    if not output:
        raise HTTPException(
            404, detail="Unable to find any deployments matching the given parameters."
        )

    return output
