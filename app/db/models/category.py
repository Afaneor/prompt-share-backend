from tortoise import fields

from db.models.abstract_model import AbstractModel


class Category(AbstractModel):
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name