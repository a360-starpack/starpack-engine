from typing import List
from fastapi import APIRouter

from ..plugengine.engine import PluginEngine

from ..schemas.plugins import PluginOut, Plugin
from ..errors import *

router = APIRouter(tags=["plugins"])


@router.get("/plugins", response_model=List[PluginOut])
async def get_plugins():
    """
    Takes in a payload dictionary of packaging steps to create a deployment.
    """

    return list(PluginEngine.plugins.values())

