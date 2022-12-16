from calculators import ProductSumCalculator, OfferCalculator
from store_model import Offer, QtyCondition
import math


class TestProductSumCalculator:
    def test_init(self):
        psc = ProductSumCalculator()

        assert hasattr(psc, 'count_of_prods')

        assert psc.sum_prods == 0

        assert isinstance(psc.count_of_prods, dict)

    def test_calculate(self):
        psc = ProductSumCalculator()

        count_of_prods = {"Prod1": {"qty": 1, "price": 10}, "Prod2": {"qty": 2, "price": 5}}

        assert psc.sum_prods == 0

        psc.update_counts(count_of_products=count_of_prods)
        psc.calculate()

        assert psc.sum_prods == 20

        assert psc.total_per_product['Prod2'] == 10


class TestOfferCalculator:

    def product_with_one_offer(self):
        offer = Offer(product='Product1', discount=0.1, condition=[], applies=math.inf, message='')

        ofc = OfferCalculator(list_of_offers=[offer])

        return ofc

    def product_with_one_offer_and_cond(self):
        offer = Offer(product='Product1', discount=0.1, condition=[QtyCondition(product="Prod2", qty=2)],
                      applies=math.inf,
                      message='')

        ofc = OfferCalculator(list_of_offers=[offer])

        return ofc

    def test_extract_relevant_product(self):
        ofc = self.product_with_one_offer()

        assert ofc.offer_relevant_product == {"Product1"}

        ofc = self.product_with_one_offer_and_cond()

        assert ofc.offer_relevant_product == {"Product1", "Prod2"}

    def test_update_counts(self):
        ofc = self.product_with_one_offer()

        ofc.update_counts({"Product1": {"price": 1.0, "qty": 1}})

        assert ofc.count_of_prods == {"Product1": {"price": 1.0, "qty": 1}}

        ofc = self.product_with_one_offer()

        ofc.update_counts({"Product1": {"price": 1.0, "qty": 1}, "Product2": {"price": 1.0, "qty": 1}})

        assert ofc.count_of_prods == {"Product1": {"price": 1.0, "qty": 1}}

    def test_arithmetic(self):

        # test simple 1 offer 1 product discount calculation

        ofc = self.product_with_one_offer()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 1}})

        offer = ofc.offers[0]

        ret = ofc.offer_arithmetic(offer=offer)

        assert ret == 0.1

        # test 1 offer 1 discount with unfulfilled condition

        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 1}, "Prod2": {"price": 1.0, "qty": 1}})
        offer = ofc.offers[0]

        ret = ofc.offer_arithmetic(offer=offer)

        assert ret == 0

        # test 1 offer 1 discount with filled condition

        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 1}, "Prod2": {"price": 1.0, "qty": 2}})
        offer = ofc.offers[0]

        ret = ofc.offer_arithmetic(offer=offer)

        assert ret == 0.1

        # test 1 offer with twice filled condition applied

        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}, "Prod2": {"price": 1.0, "qty": 4}})
        offer = ofc.offers[0]

        ret = ofc.offer_arithmetic(offer=offer)

        assert ret == 0.2

        # test 1 offer with twice filled condition but only one product to apply on (so it is applied once)

        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}, "Prod2": {"price": 1.0, "qty": 3}})
        offer = ofc.offers[0]

        ret = ofc.offer_arithmetic(offer=offer)

        assert ret == 0.1

        # test 1 offer with twice filled condition but limit on condition max 1 application per basket

        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}, "Prod2": {"price": 1.0, "qty": 4}})
        offer = ofc.offers[0]
        offer.applies = 1
        ofc.offers[0] = offer

        ret = ofc.offer_arithmetic(offer=offer)

        assert ret == 0.1

    def test_condition_lookover(self):
        # one condition check lookover
        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}, "Prod2": {"price": 1.0, "qty": 4}})
        ret = ofc.conditions_look_over(offer=ofc.offers[0])

        assert ret == 2

        # one condition check lookover

        ofc = self.product_with_one_offer_and_cond()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}, "Prod2": {"price": 1.0, "qty": 7}})
        ret = ofc.conditions_look_over(offer=ofc.offers[0])

        assert ret == 3

        # no conditions

        ofc = self.product_with_one_offer()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}})
        ret = ofc.conditions_look_over(offer=ofc.offers[0])

        assert ret == math.inf

        # two conditions
        offer = Offer(product='Product1', discount=0.1, condition=[QtyCondition(product="Prod2", qty=2),
                                                                   QtyCondition(product="Prod3", qty=1)],
                      applies=math.inf,
                      message='')

        ofc = OfferCalculator(list_of_offers=[offer])
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 2}, "Prod2": {"price": 1.0, "qty": 4},
                           "Prod3": {"price": 1.0, "qty": 4}})

        ret = ofc.conditions_look_over(offer=ofc.offers[0])

        assert ret == 2

    def test_calculate(self):
        # test full calc function

        ofc = self.product_with_one_offer()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 1}})
        ofc.calculate()

        assert ofc.total_offer_discount == 0.1

        ofc = self.product_with_one_offer()
        ofc.update_counts({"Product1": {"price": 1.0, "qty": 3}})
        ofc.calculate()

        assert ofc.total_offer_discount == 0.3

