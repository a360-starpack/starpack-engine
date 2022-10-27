from typing import Any, Dict
from fastapi import APIRouter

from ..plugengine.engine import PluginEngine

from ..schemas.payloads import StarpackInput
from ..errors import *

router = APIRouter()


@router.post("/package")
async def package(starpack_input: StarpackInput):
    # Create a plugin engine instance
    engine = PluginEngine()

    datastore: Dict[str, Any] = dict()

    if starpack_input.package is None:
        raise MissingPackageInput()

    package_input = starpack_input.package

    for step in package_input.steps:
        engine.invoke(step.type)

    return {"status": "You did it!"}
