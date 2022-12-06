from typing import List, Dict

from fastapi import APIRouter, Body

from ..engine import PluginEngine
from ..schemas.plugins import PluginOut

router = APIRouter(tags=["plugins"])


@router.get("/plugins", response_model=List[PluginOut])
async def get_plugins():
    """
    Takes in a payload dictionary of packaging steps to create a deployment.
    """

    return list(PluginEngine.plugins.values())


@router.post("/plugins/test/{plugin_name}")
async def plugin_tester(plugin_name: str, args: Dict = Body()):
    engine = PluginEngine()
    engine.invoke(plugin_name, args)
    return args
