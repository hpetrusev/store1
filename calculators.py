import typing
from abc import abstractmethod
from store_model import Offer
import math


class BaseCalculator:
    """
    base class for calculator classess

    calculations are based on counts of products
    """

    def __init__(self, **kwargs):
        self.count_of_prods: typing.Dict = dict()
        pass

    @abstractmethod
    def update_counts(self, count_of_products: typing.Dict):
        """
        :param count_of_products: dictionary with counts of products
        """
        pass

    @abstractmethod
    def calculate(self):
        """
        perform the calculation relevant for the calculator
        """
        pass


class ProductSumCalculator(BaseCalculator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sum_prods = 0
        self.total_per_product = dict()

    def update_counts(self, count_of_products: typing.Dict):
        """
        implementation of the count of products in the total sum calc
        """
        self.count_of_prods = count_of_products

    def calculate(self):
        """
        implementation of calculate, simple sum of qty X price of each product
        """
        total = 0
        for k, v in self.count_of_prods.items():
            notional = v["qty"] * v["price"]
            self.total_per_product[k] = round(notional, 2)
            total += notional

        self.sum_prods = total


class OfferCalculator(BaseCalculator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.offer_relevant_product = set()
        self.offers = []
        self.per_offer = []
        self.total_offer_discount = 0

        list_of_offers = kwargs.get("list_of_offers")
        if list_of_offers is None:
            list_of_offers = []

        for off in list_of_offers:
            self._extract_offer_relevant_products(off)

            self.offers.append(off)

    def _extract_offer_relevant_products(self, offer):
        if offer.product not in self.offer_relevant_product:
            self.offer_relevant_product.add(offer.product)

        for cond in offer.condition:
            if cond.product not in self.offer_relevant_product:
                self.offer_relevant_product.add(cond.product)

    def update_counts(self, count_of_products: typing.Dict):
        """
        implementation of update counts, filters out irrelevant counts
        """
        self.count_of_prods = {
            k: count_of_products[k]
            for k in self.offer_relevant_product
            if k in count_of_products
        }

    def calculate(self):
        """
        calculate function of the offers, goes offer by offer, calcs the total, and per offer discount
        """
        for offer in self.offers:
            from_offer = self.offer_arithmetic(offer=offer)
            self.total_offer_discount += round(from_offer, 2)
            if from_offer > 0:
                self.per_offer.append((offer.message, from_offer))

    def offer_arithmetic(self, offer: Offer):

        total = 0
        if offer.product in self.count_of_prods.keys():

            if self.count_of_prods[offer.product]["qty"] > 0:

                can_apply_to = self.conditions_look_over(offer)

                applied_on = min(
                    self.count_of_prods[offer.product]["qty"],
                    offer.applies,
                    can_apply_to,
                )
                total = (
                    applied_on * self.count_of_prods[offer.product]["price"]
                ) * offer.discount

        return total

    def conditions_look_over(self, offer: Offer):
        """
        Iterates over all conditions needed to be met for the offer to hold, and picks up the smallest number
        of fulfilled conditions, since this is the number of times that the offer can be applied.

        If no conditions for the offer it only returns positive infinity
        """
        if len(offer.condition) > 0:
            conditions_hold = []
            for cond in offer.condition:
                res = cond.check_condition(product_count_and_price=self.count_of_prods)
                conditions_hold.append(res)

            can_apply_to = min(conditions_hold)

            return can_apply_to
        else:
            return math.inf

    def __repr__(self):
        return f"<{self.offers}>"


def get_calculator(calc_needed, **kwargs):
    calcs = {
        "ProductSumCalculator": ProductSumCalculator,
        "OfferCalculator": OfferCalculator,
    }

    return calcs[calc_needed](**kwargs)
