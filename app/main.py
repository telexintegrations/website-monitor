from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import integration, tick
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(integration.router)
app.include_router(tick.router)
