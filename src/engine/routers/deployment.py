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
