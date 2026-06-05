from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controllers.reserve_controller import router as reserve_router
from backend.controllers.dataset_controller import router as dataset_router
from backend.controllers.analysis_controller import router as analysis_router
from backend.controllers.auth_controller import router as auth_router

app = FastAPI(
    title="BioSentinel API",
    description="API for environmental reserve monitoring using satellite data.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "BioSentinel API running"}


app.include_router(reserve_router)
app.include_router(dataset_router)
app.include_router(analysis_router)
app.include_router(auth_router)