from fastapi import APIRouter
from api.prompts.prompts import router as prompts_router
from api.category.category import router as category_router
router = APIRouter()

router.include_router(
    prompts_router,
    prefix="/api/prompts",
    tags=["prompts"]
)

router.include_router(
    category_router,
    prefix="/api/categories",
    tags=["category"]
)


__all__ = ["router"]
