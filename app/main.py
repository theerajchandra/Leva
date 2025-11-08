# /app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import bookings, finance, auth

# Import all models so SQLAlchemy knows about them
from app.models import organization, client, workflow, finance as finance_models

app = FastAPI(title="Leva API")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(finance.router, prefix="/api/v1/finance", tags=["Finance"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
