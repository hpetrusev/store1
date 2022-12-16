import logging
import sys
import typing
from abc import ABCMeta
from abc import abstractmethod
from enum import Enum

from calculators import get_calculator
from db_ops import get_database, Filtering, Datasets
from format_number_representation import get_formatter
from store_model import Basket, serialize_offer
import variables


class Policies(Enum):
    # one available method at the moment
    PriceBasket = "PriceBasket"


class OutputReport:
    subtotal_default = "Subtotal: "
    total_default = "Total: "
    no_offers_message = "(No offers available)"

    def __init__(self, subtotal: str, total: str, offers: typing.List = None):
        if offers is None:
            self.offers = []
        else:
            self.offers = offers
        self.subtotal = subtotal
        self.total = total

    def __repr__(self):
        if len(self.offers) == 0:
            return (
                f"===================================\n"
                f"{self.subtotal} {self.no_offers_message}\n{self.total}"
                f"\n===================================\n"
            )
        else:
            final_string = f"===================================\n{self.subtotal}\n"
            for offer in self.offers:
                final_string += f"{offer}\n"
            final_string += self.total + "\n===================================\n"
            return final_string

    @classmethod
    def create_report(
            cls,
            subtotal: float,
            total: float,
            offers: typing.List[typing.Tuple[str, float]],
            formatter: str,
    ):

        formatter = get_formatter(formatter)

        if isinstance(offers, list):
            offers = [f"{a[0]} {formatter.format_number(a[1])}" for a in offers]
        else:
            pass
        return cls(
            subtotal=cls.subtotal_default + formatter.format_number(number=subtotal),
            total=cls.total_default + formatter.format_number(number=total),
            offers=offers,
        )


class PolicyBase(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def run(self, args):
        pass


class PriceBasketPolicy(PolicyBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # get data connector

        self._db = get_database(variables.DATABASE)

        self.report = None
        self.calc_applier = None

        # create Basket
        self.basket = Basket()

    def initiate_calc_controller(self):
        # take active offers
        offers = self._db.get(
            data=Datasets.offers.value,
            filters=[Filtering(filter_by="active", filter_value=[True])],
        )

        # serialize offers
        offers = [serialize_offer(off) for off in offers]

        # calc applier, helper class to the policy class
        self.calc_applier = CalcController(
            calculators_needed=["OfferCalculator", "ProductSumCalculator"],
            list_of_offers=offers,
        )

    def get_objects_into_basket(self, args):
        if args is None:
            args = []

        for arg in args:

            filtered_obj = self._db.get(
                data=Datasets.prices.value,
                filters=[Filtering(filter_by="product", filter_value=arg)],
            )

            if len(filtered_obj) == 0:
                logging.warning(f" product {arg} unavailable")
            else:
                [self.basket.add_product(product=prod_obj) for prod_obj in filtered_obj]

    def apply_calculations(self):
        # generic apply calc

        self.calc_applier.apply_calc(self.basket.count_of_products)

        # extract needed information from the calculators

        subtotal = self.calc_applier.calculators["ProductSumCalculator"].sum_prods
        total = (
                subtotal
                - self.calc_applier.calculators["OfferCalculator"].total_offer_discount
        )
        per_offer = self.calc_applier.calculators["OfferCalculator"].per_offer

        return total, subtotal, per_offer

    def run(self, args):
        """
        PriceBasket policy run function in 4 steps;

        :param args: input arguments
        """
        self.initiate_calc_controller()

        # 1) get objects into the basket; with it create a count of objects;

        self.get_objects_into_basket(args)

        # 2) apply calculation which gives subtotal, total, and per_offer calculation

        total, subtotal, per_offer = self.apply_calculations()

        # 3) create report from the provided numbers

        self.report = OutputReport.create_report(
            total=total,
            subtotal=subtotal,
            offers=per_offer,
            formatter=variables.FORMATTER,
        )

        # 4) send the report to the stdout

        sys.stdout.write(f"{self.report}")


class CalcController:
    """
    Calculations based on count dictionaries
    """

    def __init__(self, calculators_needed, **kwargs):
        self.calculators = dict()
        for c in calculators_needed:
            self.calculators[c] = get_calculator(c, **kwargs)

    def apply_calc(self, count_dictionary):

        for c in self.calculators.keys():
            self.calculators[c].update_counts(count_dictionary)
            self.calculators[c].calculate()


def get_policy(policy_input, **kwargs) -> PolicyBase:
    policies = {"PriceBasket": PriceBasketPolicy}

    return policies[policy_input.value](**kwargs)
