from django.db import models


class Tags(models.Model):
    tag_name = models.CharField(max_length=100, unique=True)
