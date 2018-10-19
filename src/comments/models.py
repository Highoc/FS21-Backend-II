from django.db import models
from django.conf import settings

from topics.models import Topic

class Comment(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='autor_comments',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    topic = models.ForeignKey(
        Topic,
        related_name='topic_comments',
        verbose_name='Топик',
        on_delete=models.CASCADE
    )

    text = models.TextField(
        max_length=2047,
        verbose_name='Текст'
    )

    comment = models.ForeignKey(
        'self', blank=True, null=True,
        related_name='child_comments',
        verbose_name='Родительский комментарий',
        on_delete = models.CASCADE
    )

    is_archive = models.BooleanField(
        default=False,
        verbose_name='Коммент удален?'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = 'topic', 'author', 'id'

    def __unicode__(self):
        return str(self.id)
