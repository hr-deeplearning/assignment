from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from app.managers import CustomUserManager

email_regex = RegexValidator(
    regex=r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
    message="Please enter valid Email address.",
)
string_regex = RegexValidator(
    regex=r"^[a-zA-Z]+(?:\s[a-zA-Z]+)*$",
    message="Some special characters like (~!#^`'$|{}<>*) are not allowed.",
)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True, validators=[email_regex])
    first_name = models.CharField(
        max_length=50, blank=True, null=True, validators=[string_regex]
    )
    last_name = models.CharField(
        max_length=50, blank=True, null=True, validators=[string_regex]
    )
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        return

    def __str__(self):
        return self.email


class Contact(models.Model):

    fullname = models.CharField(max_length=255)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_user = models.ForeignKey(
        CustomUser, related_name="contacts", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.fullname


phone_validator = RegexValidator(
    regex=r"^\d*$",
    message="Phone number Up to 12 digits allowed.",
)


class ContactPhone(models.Model):

    contact = models.ForeignKey(
        Contact, related_name="phones", on_delete=models.CASCADE
    )
    number = models.CharField(validators=[phone_validator], max_length=12)
    is_deleted = models.BooleanField(default=False)
    created_user = models.ForeignKey(
        CustomUser, related_name="phones", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.number

    def __eq__(self, obj):
        return self.number == obj.number

    def __hash__(self):
        return hash(self.number)
