from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver,Signal
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Sum
from django import forms
from django.forms import ValidationError

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
    balance = models.DecimalField(default=0.00,decimal_places=2,max_digits=15)
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
        return f"{self.virtualwallet}-{self.owner}"

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

class sendcoin(models.Model):
    sender =  models.CharField(max_length=150, default=None)
    receiver = models.CharField(max_length=150, default=None)
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} sent {self.amount} to {self.receiver}"
    
class Log(models.Model):
    customer_name = models.CharField(max_length=30)
    customer_email = models.CharField(max_length=30,blank=True)
    status = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=20)
    narration = models.CharField(max_length=50,null=True,blank=True)
    account = models.CharField(max_length=10)
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    transaction_ref = models.CharField(max_length=35,blank=True)
    reference= models.CharField(max_length=35)
    created_at = models.CharField(max_length=26)

    def __str__(self):
        return  f"{self.transaction_type}-{self.reference}"
        

@receiver([post_save,post_delete], sender=sendcoin)
def pre_save_sendcoins(sender, instance, **kwargs):
    reseiver = instance.receiver
    xendeer =instance.sender
    xendee = Profile.objects.get(username=instance.sender)
    reseive = Profile.objects.get(username=instance.receiver)
    xendeer = wallet.objects.get(owner=xendee)
    reseiver = wallet.objects.get(owner=reseive)

    xendeer_bal = xendeer.balance - instance.amount
    reseiveer_balance = reseiver.balance + instance.amount
    print(xendeer.balance)
    print(reseive)
    print(reseiver.balance)
    xendeer.balance = xendeer_bal
    reseiver.balance = reseiveer_balance
    # xendeer.save()
    # reseiver.save()
 
    
  
    

    # wallet.balance = total
    # wallet.save(update_fields=['balance'])
    # sca.save()
    # waller_receiver.save()

