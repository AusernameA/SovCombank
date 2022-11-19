from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, phone, passport_ID, passport_Series, password=None):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone or not passport_ID or not passport_Series:
            raise ValueError('Users must have an phone ')

        user = self.model(
            phone=phone,
            passport_ID=passport_ID,
            passport_Series=passport_Series
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, passport_ID, passport_Series, password):
        """
        Creates and saves a staff user with the given phone and password.
        """
        user = self.create_user(
            phone=phone,
            passport_ID=passport_ID,
            passport_Series=passport_Series,
            password=password,
        )
        user.staff = True
        user.approved = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, passport_ID, passport_Series, password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone=phone,
            passport_ID=passport_ID,
            passport_Series=passport_Series,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.approved = True
        user.save(using=self._db)
        return user

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class User(AbstractBaseUser):
    phone = models.CharField(max_length=20, unique=True, verbose_name="телефон")
    passport_ID = models.IntegerField(verbose_name="номер паспорта")
    passport_Series = models.IntegerField(verbose_name="серия паспорта")
    time_registrate = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")
    approved = models.BooleanField(default=False, verbose_name="верифицирован")
    banned = models.BooleanField(default=False, verbose_name="забанен")
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser


    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['passport_ID', 'passport_Series']

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their phone
        return self.phone

    def get_short_name(self):
        # The user is identified by their phone
        return self.phone

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Transfers(models.Model):
    transfer_id = models.AutoField(primary_key=True, verbose_name="id перевода")
    sender = models.TextField(verbose_name="кто отправил")
    recipient = models.TextField(verbose_name="кто получил")
    amount = models.IntegerField(verbose_name="кол-во переведенных денег")
    date = models.DateField(auto_now_add=True, verbose_name="дата перевода")

    class Meta:
        verbose_name = 'перевод'
        verbose_name_plural = 'переводы'

