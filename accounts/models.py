import uuid
from django.db import models
from accounts.functions import generate_fields
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/{filename}'

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)
    usertype =models.CharField(
        max_length=20,
        choices=(
            ("management", "Management"),
            ("student", "Student"),
            ("teacher", "Teacher"),
            ("worker", "Worker"),
            ("accountant", "Accountant"),
        ),
        default="student",
    )
    enc_key = models.UUIDField(default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to="photo", blank=True, null=True)

    def get_fields(self):
        return generate_fields(self)

    class Meta:
        # Define the app_label if needed
        app_label = 'accounts'

    # Specify custom related names to resolve the clash
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("main:customer_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:customer_delete", kwargs={"pk": self.pk})
