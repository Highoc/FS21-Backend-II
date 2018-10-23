from django.db import models
from django.conf import settings

from categories.models import Category

class TopicQueryset(models.QuerySet):

    def annotate_everything(self):
        qs = self.select_related("author")
        qs = qs.prefetch_related("categories", "topic_likes", "topic_likes__author")
        #qs = qs.annotate(likes_count=models.Count('topic_likes'))
        return qs

    def get_stats(self):
        return self.aggregate(all_topic_count=models.Count('id'))

class Topic(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='topics',
        verbose_name='Автор топика',
        on_delete = models.CASCADE
    )

    text = models.TextField(
        max_length=40980,
        verbose_name='Текст топика'
    )

    categories = models.ManyToManyField(
        Category,
        related_name='topics',
        verbose_name='Категория'
    )

    name = models.CharField(
        max_length=127,
        verbose_name='Название топика'
    )

    is_archive = models.BooleanField(
        default=False,
        verbose_name='В архиве?'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано?"
    )

    viewcount = models.IntegerField(
        default=0,
        verbose_name='Просмотры'
    )

    objects = TopicQueryset.as_manager()

    class Meta:
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'
        ordering = 'name', 'id'

    def __unicode__(self):
        return self.name