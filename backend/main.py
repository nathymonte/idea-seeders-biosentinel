from fastapi import FastAPI

from backend.controllers.reserve_controller import router as reserve_router
from backend.controllers.dataset_controller import router as dataset_router
from backend.controllers.analysis_controller import router as analysis_router


app = FastAPI(
    title="BioSentinel API",
    description="API for environmental reserve monitoring using satellite data.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "BioSentinel API running"}


app.include_router(reserve_router)
app.include_router(dataset_router)
app.include_router(analysis_router)