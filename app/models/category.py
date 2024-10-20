from tortoise.contrib.pydantic import pydantic_model_creator


from db.models.prompt import Category

CategoryPydantic = pydantic_model_creator(
    Category,
    exclude=('updated_at',),
)

