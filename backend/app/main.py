from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_tables
from app.api import auth, doctors, credits, transactions, dashboard, profile, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create all tables
    create_tables()
    yield
    # Shutdown (nothing to do)


app = FastAPI(
    title="Doctor Data Platform API",
    description="""
    ## Doctor Data Platform — Multiplier AI Assessment
    
    A credit-based doctor discovery platform. Users purchase credits, then use them to unlock detailed doctor profiles.
    
    > **Note:** All payments are simulated for demo purposes. All doctor data is fictional.
    
    ### Authentication
    Use the `/api/auth/login` endpoint to get a JWT token, then click **Authorize** and enter `Bearer <token>`.
    
    ### Demo Credentials
    - **User:** user@demo.com / Demo@1234
    - **Admin:** admin@demo.com / Admin@1234
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(credits.router, prefix="/api/credits", tags=["Credits"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Doctor Data Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "doctor-data-platform"}
