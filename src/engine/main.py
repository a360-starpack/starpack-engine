import fastapi
from .routers import test_plugins

app = fastapi.FastAPI(
    title="Starpack Engine by Andromeda 360",
    description="An extensible engine to package and deploy ML models",
    version="0.0.1",
)

app.include_router(test_plugins.router)


@app.get("/healthcheck")
async def hello_world():
    return {"healthy": True}
