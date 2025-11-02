from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


class UserManager(BaseUserManager):
    """Custom user manager for User model."""

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("ユーザー名は必須です。"))
        if not password:
            raise ValueError(_("パスワードは必須です。"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("管理者ユーザーは is_staff=True である必要があります。"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("管理者ユーザーは is_superuser=True である必要があります。")
            )

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(
        verbose_name=_("ユーザー名"),
        max_length=150,
        unique=True,
        help_text=_(
            "ユーザー名は必須です。150文字以内。英字、数字、@/./+/-/_ のみ使用可能です。"
        ),
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message=_(
                    "有効なユーザー名を入力してください。この値には英字、数字、@/./+/-/_ 文字のみを含めることができます。"
                ),
            )
        ],
        error_messages={
            "unique": _("そのユーザー名は既に存在します。"),
            "blank": _("このフィールドは必須です。"),
        },
    )
    nickname = models.CharField(
        verbose_name=_("ニックネーム"),
        max_length=30,
        unique=True,
        default=f"匿名{uuid4().hex[:12]}",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("ユーザー")
        verbose_name_plural = _("ユーザ一一覧")

    def __str__(self):
        return self.username
