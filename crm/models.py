from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django_countries.fields import CountryField


# Create your models here.


class CustomerSource(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    A model for a base customer.

    Contents everything, related to CRM via properties:
        * payments: payment history: :model:`history.PaymentEvent`
        * classes: all bought classes: :model:`hub.Class`
        * subscriptions: all bought subscriptions: :model:`hub.Subscription`

    The model automatically assigned to a current user, so you can access all CRM properties via `request.user.crm`.
    """
    LEVELS = [(a + str(i), a + str(i)) for i in range(1, 4) for a in ('A', 'B', 'C')]

    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, related_name='crm')

    source = models.CharField(max_length=140, default='internal')

    customer_first_name = models.CharField('First name', max_length=140, blank=True)
    customer_last_name = models.CharField('Last name', max_length=140, blank=True)
    customer_email = models.EmailField('Email', blank=True)

    date_arrived = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(null=True, blank=True)

    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    profession = models.CharField(max_length=140, null=True, blank=True)

    country = CountryField()
    native_language = models.CharField(max_length=140, null=True, blank=True)

    starting_level = models.CharField(max_length=2, db_index=True, choices=LEVELS, default='A1')
    current_level = models.CharField(max_length=2, db_index=True, choices=LEVELS, default='A1')

    skype = models.CharField('Skype login', max_length=140, blank=True)
    facebook = models.CharField('Facebook profile id', max_length=140, blank=True)
    twitter = models.CharField('Twitter username', max_length=140, blank=True)
    instagram = models.CharField('Instagram username', max_length=140, blank=True)
    linkedin = models.CharField('Linkedin username', max_length=140, blank=True)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def email(self):
        return self._get_user_property('email')

    @property
    def first_name(self):
        return self._get_user_property('first_name')

    @property
    def last_name(self):
        return self._get_user_property('last_name')

    def _get_user_property(self, property):
        """
        Some properties are stored in the stock Django user model. This method
        fetches a property from the user model if user is composited,
        and fetches a customer field if not.

        Please don't forget to exclude this fields from admin form defined in
        `crm.admin`
        """
        if self.user:
            return getattr(self.user, property)
        return getattr(self, 'customer_' + property)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Lead'


class RegisteredCustomer(Customer):
    """
    A stub customer model for administration purposes
    """
    @property
    def bought_classes(customer):
        return customer.classes.filter(buy_source=0).count()  # select only single bought classes

    @property
    def bought_subscriptions(customer):
        return customer.subscriptions.count()

    class Meta:
        proxy = True
        verbose_name = 'Student'


@receiver(pre_save, sender=User)
def create_customer(sender, **kwargs):
    """
    TODO check if this is still needed
    """
    user = kwargs.get('instance')
    if not user.pk:
        customer = Customer()
        customer.save()
        user.crm = customer
