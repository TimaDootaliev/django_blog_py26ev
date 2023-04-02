from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Укажите username')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    # Создаем функцию для создания обычного пользователя
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(username, email, password, **extra_fields)
    
    # Создаем функцию для создания суперпользователя
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(username, email, password, **extra_fields)


# Создаем класс пользователей на основе стандартной модели Django AbstractBaseUser
class CustomUser(AbstractBaseUser):
    # Определяем поля модели
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) # админ
    activation_code = models.CharField(max_length=10, blank=True) # blank - обязательно ли к заполнению

    REQUIRED_FIELDS = ['email']

    USERNAME_FIELD = 'username'

    # Указываем объект менеджера пользователей
    objects = CustomUserManager()

    # Функции проверки прав пользователя
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff
    
    # Определяем метаданные модели
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

