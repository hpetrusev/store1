import typing
from dataclasses import dataclass
from abc import abstractmethod
import math


@dataclass
class Product:
    """
    Product representation; supports native addition
    """

    name: str
    price: float

    def __add__(self, other):
        if isinstance(other, Product):
            return self.price + other.price
        else:
            return self.price + other

    __radd__ = __add__


class Condition:
    """
    base class of condition (can be used to filter conditions)
    """

    product: str

    @abstractmethod
    def check_condition(self, product_count_and_price):
        pass


@dataclass
class QtyCondition(Condition):
    """
    conditions by quantity per product
    """

    product: str
    qty: float

    def check_condition(self, product_count_and_price):
        res = int(math.floor(product_count_and_price[self.product]["qty"] / self.qty))
        return res


@dataclass
class Offer:
    """
    Offer representation
    """

    product: str  # name of the product
    discount: float  # discount fraq from 0 to 1.0
    condition: typing.List[Condition]  # condition requirement/s
    applies: typing.Union[int, float]  # even if all conditions are fulfilled, how many max does it apply to (-1 indicated no limit)
    message: str  # message of the offer for the user


def serialize_conditions(list_of_conditions) -> typing.List[Condition]:
    """
    :param list_of_conditions: dictionary version of the conditions in a list
    :param list_of_conditions: switch to the right condition according to criteria
     and instantiate the right condition object
    :return: list of conditions in the programs native objects
    """
    list_of_conditions_serialized = []
    for cond in list_of_conditions:
        if "product" and "qty" in cond.keys():
            serialized_cond = QtyCondition(product=cond["product"], qty=cond["qty"])

            list_of_conditions_serialized.append(serialized_cond)

    return list_of_conditions_serialized


def serialize_offer(offer) -> Offer:
    """
    :param offer: raw offer dictionary
    :return: offer in the programs native object
    """
    conditions = offer["condition"]

    list_of_conditions = serialize_conditions(conditions)

    if offer["applies"] == -1:
        applies = math.inf
    else:
        applies = offer["applies"]

    serialized_offer = Offer(
        product=offer["product"],
        discount=offer["discount"],
        condition=list_of_conditions,
        applies=applies,
        message=offer["message"],
    )

    return serialized_offer


def serialize_prod(prod_unserialized: typing.Dict) -> Product:
    """
    :param prod_unserialized: dictionary version of the product/item
    :return: product/item in the programs native object form
    """
    prod_serialized = Product(
        name=prod_unserialized["product"], price=prod_unserialized["price"]
    )
    return prod_serialized


class Basket:
    """
    Entrypoint class for items in the form of raw data inputs; In this class they are stored,
    and are getting translated to the objects of the program.

    keeps 1) dictionary of counts; and 2) a list of products;


    count of products is a dictionary in the following form
    {"Prod1": {"qty": 1, "price": 10}, "Prod2": {"qty": 2, "price": 5}}

    """

    def __init__(self):
        self.list_of_products: typing.List[Product] = []
        self.count_of_products = dict()

    def add_product(self, product: dict):
        """
        Appends products to the list of products and appends the count

        :param product: dictionary format of the product/item
        """
        prod_serialized = serialize_prod(prod_unserialized=product)
        if prod_serialized.name not in self.count_of_products.keys():
            self.count_of_products[prod_serialized.name] = {
                "qty": 1,
                "price": prod_serialized.price,
            }
        else:
            self.count_of_products[prod_serialized.name]["qty"] += 1

        self.list_of_products.append(prod_serialized)

    def __iter__(self):
        for prd in self.list_of_products:
            yield prd

    def __repr__(self):
        return f"{self.list_of_products}"
