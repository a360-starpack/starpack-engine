import fastapi
from .routers import test_plugins, package
from .plugengine import PluginEngine
from . import __version__

app = fastapi.FastAPI(
    title="Starpack Engine by Andromeda 360",
    description="An extensible engine to package and deploy ML models",
    version=__version__,
)

# Add the routes for all specialized routers
app.include_router(test_plugins.router)
app.include_router(package.router)


@app.patch("/plugins")
@app.on_event("startup")
def initialize_plugins():
    plugin_engine = PluginEngine()
    plugin_engine._discover()
    plugin_engine._load()


@app.get("/healthcheck")
async def hello_world():
    return {"healthy": True}
