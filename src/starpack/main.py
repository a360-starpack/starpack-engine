import fastapi

app = fastapi.FastAPI(
    title="Starpack Engine by Andromeda 360",
    description="An extensible engine to package and deploy ML models",
    version="0.0.1",
)


@app.get("/healthcheck")
def hello_world():
    return {"healthy": True}
