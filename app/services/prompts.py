from typing import Optional, Literal

from fastapi_pagination.ext.tortoise import paginate
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import F, Q

from db.models import Prompt
from models.prompt import PromptPydantic, PromptInPydantic


class PromptException(Exception):
    pass


async def list_all_prompts(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    sort_by_rating: Literal['desc', ''] = '',
) -> PromptPydantic:
    # Начальный базовый запрос
    query = Prompt.all().prefetch_related("categories")

    # Фильтрация по категории
    if category_id:
        query = query.filter(categories__id=category_id)

    # Поиск по названию и описанию
    if search:
        query = query.filter(
            Q(title__icontains=search) | Q(description__icontains=search),
        )

    # Сортировка по рейтингу (по умолчанию по возрастанию, можно передавать sort_by_rating=desc для убывания)
    if sort_by_rating:
        query = query.order_by(f"{'-' if sort_by_rating == 'desc' else ''}rating")

    return await paginate(query)

async def get_single_prompt(prompt_id: int) -> PromptPydantic:
    try:
        prompt = await PromptPydantic.from_queryset_single(
            Prompt.get(id=prompt_id).prefetch_related("categories"),
        )
    except DoesNotExist:
        raise PromptException("Prompt not found")
    return prompt


async def create_prompt(prompt: PromptInPydantic):
    prompt_obj = await Prompt.create(
        **prompt.model_dump(exclude_unset=True),
    )
    return await PromptPydantic.from_tortoise_orm(prompt_obj)


async def rate_prompt(prompt_id: int) -> PromptPydantic:
    await Prompt.filter(id=prompt_id).update(rating=F('rating') + 1)
    prompt = await Prompt.get(id=prompt_id)
    return await PromptPydantic.from_tortoise_orm(prompt)
