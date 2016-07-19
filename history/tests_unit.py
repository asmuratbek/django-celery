from django.test import TestCase

from elk.utils.test import mock_request, test_customer
from history.models import PaymentEvent
from hub.models import Class, Subscription
from lessons.models import OrdinaryLesson
from products.models import Product1 as product


class TestEvent(TestCase):
    fixtures = ('crm', 'products', 'lessons')
    TEST_PRODUCT_ID = 1

    def test_storing_request(self):
        """
        Unit test for populating log entry model with request.
        """
        mocked_request = mock_request()
        ev = PaymentEvent()
        ev._HistoryEvent__store_request(mocked_request)

        # Assertions are based on fixtures, generated by elk.utils.test.mock_request
        self.assertEqual(ev.is_mobile, mocked_request.user_agent.is_mobile)
        self.assertEqual(ev.is_tablet, mocked_request.user_agent.is_tablet)
        self.assertEqual(ev.is_pc, mocked_request.user_agent.is_pc)

        self.assertEqual(ev.browser_family, 'Mobile Safari')
        self.assertEqual(ev.browser_version, '5.2')
        self.assertEqual(ev.os_family, 'WinXP')
        self.assertEqual(ev.os_version, '5.3')
        self.assertEqual(ev.device, 'iPhone')

        self.assertEqual(ev.raw_useragent, 'WinXP; U/16')
        self.assertEqual(ev.ip, '127.0.0.5')

    def test_single_lesson_log_entry_creation(self):
        """
        Buy a single lesson and find a respective log entry for it
        """
        customer = test_customer()
        self.assertEqual(customer.payments.count(), 0)

        c = Class(
            customer=customer,
            lesson=OrdinaryLesson.get_default(),
            buy_price=10,
            buy_source=0,
        )
        c.request = mock_request()
        c.save()

        self.assertEqual(customer.payments.count(), 1)
        self.assertEqual(customer.payments.all()[0].product, c)

    def test_subscription_log_entry_creation(self):
        """
        Buy a subscription and find a respective log entry for it
        """
        customer = test_customer()
        self.assertEqual(customer.payments.count(), 0)

        s = Subscription(
            customer=customer,
            product=product.objects.get(pk=self.TEST_PRODUCT_ID),
            buy_price=150,
        )
        s.request = mock_request(customer=customer)
        s.save()

        self.assertEqual(customer.payments.count(), 1, 'Check if only one log record appeared: for the subscription, not for classes')
        self.assertEqual(customer.payments.all()[0].product, s)
