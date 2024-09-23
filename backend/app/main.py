from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, admin, tenants
from app.database import engine, Base

# Import all models to ensure they are registered
from app.models.user import User
from app.models.message import Message
from app.models.payment import Payment  # Import other models as needed

app = FastAPI()
Base.metadata.create_all(bind=engine)           

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Include routers for different functionalities
app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")
app.include_router(tenants.router)

# Define a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI React App!"}