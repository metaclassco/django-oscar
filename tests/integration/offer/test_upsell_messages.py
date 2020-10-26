from decimal import Decimal as D

from django.utils.timezone import now

from oscar.apps.offer.applicator import Applicator
from oscar.test import factories
from oscar.test.testcases import WebTestCase

from oscar.core.loading import get_class

Selector = get_class('partner.strategy', 'Selector')


class TestUpsellMessages(WebTestCase):

    def setUp(self):
        super().setUp()

        self.basket = factories.create_basket(empty=True)

        # Create range and add one product to it.
        rng = factories.RangeFactory(name='All products', includes_all_products=True)
        self.product = factories.ProductFactory()
        rng.add_product(self.product)

        # Create offer #1.
        condition1 = factories.ConditionFactory(
            range=rng, type=factories.ConditionFactory._meta.model.COUNT, value=D('2'),
        )
        benefit1 = factories.BenefitFactory(
            range=rng, type=factories.BenefitFactory._meta.model.MULTIBUY, value=None,
        )
        self.offer1 = factories.ConditionalOfferFactory(
            condition=condition1, benefit=benefit1,
            slug='offer-1',
            start_datetime=now(),
            name='Test offer #1',
            priority=1,
        )

        # Create offer #2.
        condition2 = factories.ConditionFactory(
            range=rng, type=factories.ConditionFactory._meta.model.COUNT, value=D('1'),
        )
        benefit2 = factories.BenefitFactory(
            range=rng, type=factories.BenefitFactory._meta.model.PERCENTAGE, value=D('5'),
        )
        self.offer2 = factories.ConditionalOfferFactory(
            condition=condition2,
            benefit=benefit2,
            slug='offer-2',
            start_datetime=now(),
            name='Test offer #2',
        )

        # Create offer #3.
        condition3 = factories.ConditionFactory(
            range=rng, type=factories.ConditionFactory._meta.model.COUNT, value=D('1'),
        )
        benefit3 = factories.BenefitFactory(
            range=rng, type=factories.BenefitFactory._meta.model.MULTIBUY, value=None,
        )
        self.offer3 = factories.ConditionalOfferFactory(
            condition=condition3,
            benefit=benefit3,
            slug='offer-3',
            start_datetime=now(),
            name='Test offer #3',
            exclusive=False,
        )

        # Create offer #4.
        condition4 = factories.ConditionFactory(
            range=rng, type=factories.ConditionFactory._meta.model.COUNT, value=D('1'),
        )
        benefit4 = factories.BenefitFactory(
            range=rng, type=factories.BenefitFactory._meta.model.MULTIBUY, value=None,
        )
        self.offer4 = factories.ConditionalOfferFactory(
            condition=condition4,
            benefit=benefit4,
            slug='offer-4',
            start_datetime=now(),
            name='Test offer #4',
            exclusive=False,
            priority=3,
        )

    def add_product(self):
        self.basket.add_product(self.product)
        self.basket.strategy = Selector().strategy()
        Applicator().apply(self.basket)

    def test_upsell_messages(self):
        """
        Checks correctness of upsell messages for the offers based on the number
        of products in the basket.

        * Offer #1 - priority = 1, exclusive, requires 2 products.
        * Offer #2 - priority = 0, exclusive, requires 1 product.
        * Offer #3 - priority = 0, non-exclusive, requires 1 product.
        * Offer #4 - priority = 3, non-exclusive, requires 1 product.
        """

        # The basket is empty. No offers are applied.
        self.assertEqual(self.offer1.get_upsell_message(self.basket), 'Buy 2 more products from All products')
        self.assertEqual(self.offer2.get_upsell_message(self.basket), 'Buy 1 more product from All products')
        self.assertEqual(self.offer3.get_upsell_message(self.basket), 'Buy 1 more product from All products')
        self.assertEqual(self.offer4.get_upsell_message(self.basket), 'Buy 1 more product from All products')

        self.add_product()

        # 1 product in the basket. Offer #4 (with the highest priority) and offer #3 are applied.
        self.assertEqual(self.offer1.get_upsell_message(self.basket), 'Buy 2 more products from All products')
        self.assertEqual(self.offer2.get_upsell_message(self.basket), 'Buy 1 more product from All products')
        for offer in [self.offer3, self.offer4]:
            self.assertIsNone(offer.get_upsell_message(self.basket), msg=offer.name)

        self.add_product()

        # 2 products in the basket. Offers #4, offer #3 and #2 are applied.
        self.assertEqual(self.offer1.get_upsell_message(self.basket), 'Buy 1 more product from All products')
        for offer in [self.offer2, self.offer3, self.offer4]:
            self.assertIsNone(offer.get_upsell_message(self.basket), msg=offer.name)

        self.add_product()

        # 3 products in the basket. Offers #4, offer #3 and #1 are applied.
        self.assertEqual(self.offer2.get_upsell_message(self.basket), 'Buy 1 more product from All products')
        for offer in [self.offer1, self.offer3, self.offer4]:
            self.assertIsNone(offer.get_upsell_message(self.basket), msg=offer.name)

        self.add_product()

        # 4 products in the basket. All the offers are applied.
        for offer in [self.offer1, self.offer2, self.offer3, self.offer4]:
            self.assertIsNone(offer.get_upsell_message(self.basket), msg=offer.name)
