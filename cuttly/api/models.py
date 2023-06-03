import uuid

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

from cuttly.settings import HOST


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    is_online = models.BooleanField(default=False)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"))

    def is_owner(self, id):
        if self.url_set.filter(id=id).first():
            return True
        return False


class URL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    original_url = models.CharField(max_length=2048)
    cutted_url = models.CharField(max_length=256, null=True, blank=True)
