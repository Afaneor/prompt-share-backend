from tortoise.contrib.pydantic import pydantic_model_creator


from db.models.prompt import Prompt

PromptPydantic = pydantic_model_creator(
    Prompt,
    exclude=('updated_at',),
)

PromptInPydantic = pydantic_model_creator(
    Prompt,
    name='PromptInPydantic',
    exclude_readonly=True,
    exclude=('updated_at', 'rating'),
)
