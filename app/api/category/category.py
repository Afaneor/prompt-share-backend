from fastapi import APIRouter
from starlette.responses import Response

from models.category import CategoryPydantic
from services.category import list_all_categories

router = APIRouter()


@router.get("/")
async def list_categories() -> list[CategoryPydantic]:
    return await list_all_categories()
