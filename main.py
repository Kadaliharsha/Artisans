from fastapi import FastAPI
from database.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
import os
from models.user import User
from models.product import Product

# import models to register them with Base
# if os.getenv("ENVIRONMENT") != "production":
#     print("🚀 Development mode: Dropping and creating tables...")
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     print("✅ Tables created!")

app = FastAPI(
    title="Artisans Hub API",
    description="E-commerce platform connecting artisans",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers.users import router as users_router
from routers.products import router as products_router
from routers.auth import router as auth_router

app.include_router(users_router)
app.include_router(products_router)
app.include_router(auth_router)

@app.get("/")
def read():
    return {"message": "Artisans Hub API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

