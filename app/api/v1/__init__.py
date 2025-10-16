from fastapi import APIRouter
from app.api.v1 import employees

api_router = APIRouter()

# Incluir routers de diferentes recursos
api_router.include_router(employees.router)