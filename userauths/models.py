from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save

from django.contrib.auth.models import UserManager as BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # optional username fallback
        extra_fields.setdefault("username", email.split("@")[0])

        return self.create_user(email, password, **extra_fields)

def user_directory_path(instance, filename):

    user = None

    # Check if instance has a direct user
    if hasattr(instance, 'user') and instance.user:
        user = instance.user
    # Check if instance has a product with a user
    elif hasattr(instance, 'product') and hasattr(instance.product, 'user') and instance.product.user:
        user = instance.product.user

    ext = filename.split('.')[-1]  # file extension

    if user:
        filename = f"{user.id}.{ext}"
        return f"user_{user.id}/{filename}"
    else:
        # fallback path for unknown user
        filename = f"file.{ext}"
        return f"user_file/{filename}"

class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=100,
        null=True,
        blank=True
    )
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        unique=True
    )
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(
        verbose_name="شماره تلفن",
        max_length=11,
        unique=True,
        null=True,
        blank=True
    )

    otp = models.CharField(
        max_length=7,
        verbose_name="کد تایید",
        blank=True,
        null=True
        
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    # Authentication settings
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        # Auto generate username from email
        if self.email and "@" in self.email:
            email_username = self.email.split("@")[0]

        if not self.full_name:
            self.full_name = email_username

        if not self.username:
            self.username = email_username

        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image", default="default/default-user.jpg", null=True, blank=True)

    full_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    pid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=12,
        alphabet="abcdefgh"
    )

    def __str__(self):
        return str(self.full_name) if self.full_name else str(self.user.full_name)

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.full_name

        super().save(*args, **kwargs)



# Signals
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



