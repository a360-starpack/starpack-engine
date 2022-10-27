from ..plugengine import PluginEngine
from fastapi import APIRouter

router = APIRouter()


@router.get("/test-plugin")
async def test_plugin(plugin_name: str):
    engine = PluginEngine()
    return engine.invoke(plugin_name)
