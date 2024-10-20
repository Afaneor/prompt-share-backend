from typing import Optional, Literal

from fastapi import APIRouter, Query
from fastapi_pagination import LimitOffsetPage
from starlette.responses import Response

from models.prompt import PromptPydantic, PromptInPydantic
from services.prompts import list_all_prompts, get_single_prompt, \
    PromptException, create_prompt, rate_prompt

router = APIRouter()

@router.get("/")
async def list_prompts(
    category_id: Optional[int] = Query(
        None,
                                       description="ID категории для фильтрации",
    ),
    search: Optional[str] = Query(None,
                                  description="Поиск по названию или описанию"),
    sort_by_rating: Literal['desc', ''] = Query(None,
                                          description="Сортировка по рейтингу ('asc' или 'desc')")
) -> LimitOffsetPage[PromptPydantic]:
    return await list_all_prompts(
        category_id=category_id,
        search=search,
        sort_by_rating=sort_by_rating,
    )


@router.get(
    "/{prompt_id}",
    responses={404: {"description": "Prompt not found"}},
)
async def get_prompt(prompt_id: int) -> PromptPydantic:
    try:
        prompt = await get_single_prompt(prompt_id)
    except PromptException as e:
        return Response('Нет такого промпта', status_code=404)
    return prompt



@router.post("/")
async def create(
    prompt: PromptInPydantic,
) -> PromptPydantic:
    return await create_prompt(prompt)


@router.post(
    "/{prompt_id}/rate",
    responses={404: {"description": "Prompt not found"}},
)
async def rate(
    prompt_id: int,
) -> PromptPydantic:
    try:
        prompt = await rate_prompt(prompt_id)
    except PromptException as e:
        return Response('Нет такого промпта', status_code=404)
    return prompt
