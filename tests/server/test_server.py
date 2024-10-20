import pytest
from db.models import Prompt, Category


@pytest.mark.asyncio
async def test_create_prompt(
    async_client
):
    # Тест на создание нового промпта
    response = await async_client.post(  # Асинхронный вызов
        "/api/prompts/",
        json={
            "title": "Test Prompt",
            "description": "This is a test prompt",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Prompt"
    assert data["description"] == "This is a test prompt"
    assert data["rating"] == 0

@pytest.mark.asyncio
async def test_list_prompts(
    async_client,
):
    # Создаем несколько промптов для теста
    await Prompt.create(
        title="First Prompt", description="First prompt description", rating=3
    )
    await Prompt.create(
        title="Second Prompt", description="Second prompt description", rating=4
    )

    # Проверяем, что список промптов возвращается корректно
    response = await async_client.get("/api/prompts/")  # Асинхронный вызов
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['items'], list)
    assert len(data['items']) == 2
    assert data['items'][0]["title"] == "First Prompt"
    assert data['items'][1]["title"] == "Second Prompt"

@pytest.mark.asyncio
async def test_get_single_prompt(
    async_client,
):
    # Создаем промпт
    prompt = await Prompt.create(
        title="Another Prompt", description="Another test prompt", rating=4
    )

    # Получаем промпт по ID
    response = await async_client.get(f"/api/prompts/{prompt.id}")  # Асинхронный вызов
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Another Prompt"
    assert data["description"] == "Another test prompt"
    assert data["rating"] == 4

@pytest.mark.asyncio
async def test_get_nonexistent_prompt(
    async_client,
):
    # Проверяем запрос несуществующего промпта
    response = await async_client.get("/api/prompts/9999")  # Асинхронный вызов
    assert response.status_code == 404
    assert response.text == 'Нет такого промпта'


@pytest.mark.asyncio
async def test_rate_prompt(
    async_client,
):
    # Создаем промпт
    prompt = await Prompt.create(
        title="Yet Another Prompt", description="Yet another test prompt", rating=0
    )

    # Оцениваем промпт
    response = await async_client.post(f"/api/prompts/{prompt.id}/rate")
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 1


@pytest.mark.asyncio
async def test_filter_prompts(
    async_client,
):
    # Создаем несколько промптов для теста
    await Prompt.create(
        title="First Prompt", description="First prompt description", rating=3
    )
    await Prompt.create(
        title="Second Prompt", description="Second prompt description", rating=4
    )

    # Проверяем фильтрацию по категории
    response = await async_client.get("/api/prompts/?category_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['items'], list)
    assert len(data['items']) == 0

    # Проверяем поиск по названию и описанию
    response = await async_client.get("/api/prompts/?search=First")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['items'], list)
    assert len(data['items']) == 1
    assert data['items'][0]["title"] == "First Prompt"

    # Проверяем сортировку по рейтингу
    response = await async_client.get("/api/prompts/?sort_by_rating=desc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['items'], list)
    assert len(data['items']) == 2
    assert data['items'][0]["title"] == "Second Prompt"
    assert data['items'][1]["title"] == "First Prompt"

@pytest.mark.asyncio
async def test_list_all_categories(
    async_client,
):
    # Создаем несколько промптов для теста
    await Category.create(name="First Category")

    # Проверяем, что список промптов возвращается корректно
    response = await async_client.get("/api/categories/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "First Category"
