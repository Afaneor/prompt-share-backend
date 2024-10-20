from db.models import Category
from models.category import CategoryPydantic


async def list_all_categories() -> CategoryPydantic:
    return await CategoryPydantic.from_queryset(
        Category.all(),
    )
