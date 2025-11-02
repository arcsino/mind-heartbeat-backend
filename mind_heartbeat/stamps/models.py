from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from uuid import uuid4


class Stamp(models.Model):
    """Stamp model."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("スタンプ名"),
        max_length=100,
        unique=True,
        help_text=_("スタンプ名は必須です。固有の名前を指定してください。"),
    )
    score = models.IntegerField(
        verbose_name=_("スコア"),
        default=0,
        help_text=_("スタンプのスコアを整数で指定してください。"),
    )
    created_at = models.DateTimeField(verbose_name=_("作成日時"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("更新日時"), auto_now=True)

    class Meta:
        verbose_name = _("スタンプ")
        verbose_name_plural = _("スタンプ一覧")

    def __str__(self):
        return self.name


class Feeling(models.Model):
    """Feeling model."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    stamp = models.ForeignKey(
        Stamp,
        verbose_name=_("スタンプ"),
        on_delete=models.CASCADE,
        related_name="feelings",
    )
    comment = models.TextField(
        verbose_name=_("コメント"),
        max_length=500,
        blank=True,
        help_text=_("気持ちに関するコメントを入力してください。"),
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("作成者"),
        on_delete=models.CASCADE,
        related_name="feelings",
    )
    created_at = models.DateTimeField(verbose_name=_("作成日時"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("更新日時"), auto_now=True)

    class Meta:
        verbose_name = _("気持ち")
        verbose_name_plural = _("気持ち一覧")

    def __str__(self):
        return f"{self.created_by.username}の気持ち - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
