from tortoise import fields

from db.models.abstract_model import AbstractModel
from db.models.category import Category


class Prompt(AbstractModel):
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    rating = fields.IntField(default=0)
    categories: fields.ManyToManyRelation['Category'] = fields.ManyToManyField(
        'server.Category',
        related_name='prompts',
    )

    def __str__(self):
        return self.title