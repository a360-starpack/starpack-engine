from ..plugengine.engine import PluginEngine
from fastapi import APIRouter

router = APIRouter()


@router.get("/test-plugin")
async def test_plugin():
    engine = PluginEngine()
    engine._discover()
    engine._load()
    return engine.invoke("example_plugin")
