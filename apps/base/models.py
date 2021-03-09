from django.db import models

class BaseModel(models.Model):

    # Una marca de tiempo que representa cuándo se creó este objeto.
    created_at = models.DateTimeField(auto_now_add=True)

    # Una marca de tiempo que representa cuándo se actualizo este objeto.
    updated_at = models.DateTimeField(auto_now=True)

    """
    Se definio un nuevo campo, que permitira dar de baja temporal una cuenta
    sin necesidad de eliminar la cuenta completamente

    """
    state = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserBaseToken(models.Model):
    # access Token
    access_token = models.CharField(db_index=True, max_length=500, null=True, default=None)

    # refresh_token
    refresh_token = models.CharField(db_index=True, max_length=500, null=True, default=None)

    class Meta:
        abstract = True
