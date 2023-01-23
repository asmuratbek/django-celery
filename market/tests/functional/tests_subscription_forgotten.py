from datetime import timedelta
from unittest.mock import patch

from django.core import mail
from django.utils import timezone
from freezegun import freeze_time
from mixer.backend.django import mixer

from elk.utils.testing import TestCase, create_customer, create_teacher
from market import models
from market.tasks import notify_forgotten_subscription
from products import models as products


@freeze_time('2032-11-01')
class TestRemindForgottenSubscription(TestCase):
    fixtures = ('lessons', 'products')
    TEST_PRODUCT_ID = 1

    @classmethod
    def setUpTestData(cls):
        cls.customer = create_customer()
        cls.product = products.Product1.objects.get(pk=cls.TEST_PRODUCT_ID)
        cls.product.duration = timedelta(days=30)

    def setUp(self):
        self.subscription = models.Subscription(
            customer=self.customer,
            product=self.product,
            buy_price=150,
        )
        self.subscription.save()

    @patch('market.models.signals.class_scheduled.send')
    def _schedule(self, c, date, *args):
        c.timeline = mixer.blend(
            'timeline.Entry',
            lesson_type=c.lesson_type,
            teacher=create_teacher(),
            start=date,
        )
        c.save()

    def test_fresh_subscription(self):
        notify_forgotten_subscription()
        self.assertEqual(len(mail.outbox), 0)

    def test_notify_if_one_week_past(self):
        with freeze_time('2032-11-10'):  # move date to 9 days in a future
            notify_forgotten_subscription()
            self.assertEqual(len(mail.outbox), 1)

    def test_update_forgotten_notify_date_when_email_sent(self):
        with freeze_time('2032-11-10'):  # move date to 9 days in a future
            notify_forgotten_subscription()
            subscription = models.Subscription.objects.get(id=self.subscription.id)
            self.assertEqual(timezone.now(), subscription.forgotten_notify_date)

    def test_ignore_subscriptions_with_fresh_scheduled_classes(self):
        first_class = self.subscription.classes.first()
        self._schedule(first_class, self.tzdatetime(2032, 11, 9, 13, 33))
        with freeze_time('2032-11-10'):  # move date to 9 days in a future
            notify_forgotten_subscription()
            self.assertEqual(len(mail.outbox), 0)

    def test_not_notify_twice(self):
        with freeze_time('2032-11-10'):  # move date to 9 days in a future
            notify_forgotten_subscription()
            self.assertEqual(len(mail.outbox), 1)

        with freeze_time('2032-11-12'):  # move date 2 days more
            notify_forgotten_subscription()
            self.assertEqual(len(mail.outbox), 1)  # amount should not be increased

    def test_remind_second_time_when_week_has_passed_from_last_reminder(self):
        with freeze_time('2032-11-10'):  # move date to 9 days in a future
            notify_forgotten_subscription()
            self.assertEqual(len(mail.outbox), 1)

        with freeze_time('2032-11-18'):  # move date to 8 days in a future
            notify_forgotten_subscription()
            print(self.subscription.forgotten_notify_date)
            self.assertEqual(len(mail.outbox), 2)  # amount increases