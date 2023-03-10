from typing import Any, Dict, Optional

from fastapi import APIRouter

from ..engine import PluginEngine
from ..errors import *
from ..schemas.payloads import StarpackInput

router = APIRouter()


@router.post("/package")
async def create_package(starpack_input: StarpackInput):
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
    datastore["images"] = dict()

    for step in package_input.steps:
        print(f"Running {step.name}")
        datastore["step_data"] = step.dict()
        engine.invoke(step.name, datastore)
        datastore.pop("step_data")

    return {"status": "You did it!"}


@router.get("/package")
def get_packages(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
):
    engine = PluginEngine()

    output = engine.invoke(
        plugin="docker_manage_packages",
        input_data={"name": name, "version": version, "wrapper": wrapper},
        method="list",
    )

    if not output:
        raise HTTPException(
            404, detail="Unable to find any packages matching the given parameters."
        )

    return output


@router.delete("/package")
def delete_packages(
    name: str,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
):
    engine = PluginEngine()

    output = engine.invoke(
        plugin="docker_manage_packages",
        input_data={"name": name, "version": version, "wrapper": wrapper},
        method="delete",
    )

    return output
