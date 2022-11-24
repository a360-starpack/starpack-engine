import sys
from pathlib import Path

import fastapi
from fastapi.responses import JSONResponse
from .routers import package, deployment, plugins
from .engine import PluginEngine
from . import __version__

app = fastapi.FastAPI(
    title="Starpack Engine by Andromeda 360",
    description="An extensible engine to package and deploy ML models",
    version=__version__,
    docs_url="/",
)

# Add the routes for all specialized routers
app.include_router(package.router)
app.include_router(deployment.router)
app.include_router(plugins.router)


@app.exception_handler(Exception)
async def debug_exception_handler(request: fastapi.Request, exc: Exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    # Get the last line of the traceback
    while exc_tb.tb_next is not None:
        exc_tb = exc_tb.tb_next

    return JSONResponse(
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "python_file": str(Path(exc_tb.tb_frame.f_code.co_filename).resolve()),
            "line_number": exc_tb.tb_lineno,
        },
        status_code=500,
    )


@app.patch("/plugins", status_code=202)
@app.on_event("startup")
async def initialize_plugins():
    plugin_engine = PluginEngine()
    plugin_engine.discover()
    plugin_engine.load()


@app.get("/healthcheck")
async def hello_world():
    return {"healthy": True}
