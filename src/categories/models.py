from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=127,
        verbose_name='Тема категории'
    )

    description = models.TextField(
        max_length=4096,
        verbose_name='Описание категории'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    is_hidden = models.BooleanField(
        default=False,
        verbose_name='Категория скрыта?'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = 'name', 'id'

    def __unicode__(self):
        return self.name