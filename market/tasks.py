from elk.celery import app as celery
from market.models import Subscription
from market.signals import subscription_forgotten


@celery.task
def notify_forgotten_subscription():
    for subscription in Subscription.objects.forgotten():
        subscription_forgotten.send(sender=notify_forgotten_subscription, instance=subscription)
        subscription.update_forgotten_notify_date()
