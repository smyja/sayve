from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, max_length=64)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    middle_name = models.CharField(max_length=64,null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        if self.email==None:
            return "ERROR,User has no email"
        return self.email.__str__()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    @property
    def full_name(self):
        """
        Returns the first_name plus the last_name and middle_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.first_name, self.last_name, self.middle_name)

        return full_name.strip()


GENDER_CATEGORY = (
    ('U','Undefined'),
    ('F','Female'),
    ('M','Male')
                    )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=160,blank=True)
    bio = models.CharField(max_length=160,null=True,blank=True)
    location = models.CharField(max_length=30,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    gender = models.CharField(choices=GENDER_CATEGORY,max_length=2)
    signup_confirmation = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, null=True)
    phone_number=models.CharField(max_length=160,null=True,blank=True)


    def __str__(self):
        return self.user.email

    def save(self, *args, **kw):

        self.slug = slugify(f"{self.user.last_name}-{self.user.first_name}")
        super(Profile, self).save(*args, **kw)

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class wallet(models.Model):
    owner=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner', null=True)
    account_number = models.IntegerField() #deposit or withdrawal wallet
    balance = models.IntegerField(default=0)
    virtualwallet = models.IntegerField(blank=True,null=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this wallet should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    def __str__(self):
        return f"{self.account_number}"

class MoneyDeposit(models.Model):
    wallet= models.ForeignKey(wallet, on_delete=models.CASCADE, related_name='fundreceiver', null=True)
    bank_name = models.CharField(max_length=150, default=None)
    payment_reference= models.CharField(max_length=150, default=None)
    orginator_name= models.CharField(max_length=300, default=None)
    amount = models.PositiveIntegerField(default=0)
    
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet}-{self.payment_reference}"

class Verification(models.Model):
    reference = models.CharField(max_length=150, default=None)
    bvn = models.IntegerField()
    owner=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bvnowner', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bvn}"
