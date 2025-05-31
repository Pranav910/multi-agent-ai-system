from fastapi import APIRouter
from . import crm

router = APIRouter()
router.include_router(crm.router, tags=["Home", "Healthcheck"])