from store_model import serialize_offer, Offer, QtyCondition, Basket, Product, serialize_prod

class TestOffers:
    offers = [
        {
            "product": "Apples",
            "discount": 0.1,
            "condition": [],
            "applies": -1,
            "active": True,
            "message": "Apples 10% off",
        },
        {
            "product": "Bread",
            "discount": 0.5,
            "condition": [{"product": "Soup", "qty": 2}],
            "applies": 1,
            "active": True,
            "message": "2 Soups for 50% off on 1 Bread.",
        },
    ]

    def test_serialization(self):
        for offer in self.offers:
            offer_s = serialize_offer(offer=offer)
            assert isinstance(offer_s, Offer)
            assert offer_s.product == offer["product"]


class TestProduct:

    product = {"product": "Milk", "price": 1.3}
    def test_product_serialize(self):
        prd = serialize_prod(self.product)
        assert isinstance(prd, Product)
        assert prd.name == 'Milk'
        assert prd.price == 1.3

    def test_product_add(self):
        p = Product(name="Milk", price=1)
        p2 = Product(name="Milk", price=1)

        assert p + p2 == 2

        assert p + p2 + 2.0 == 4.0

        assert sum([p, p2]) == 2


class TestConditions:
    def test_qty_condition(self):

        qc = QtyCondition(product='Prod1', qty=1)

        counts = {"Prod1": {"price": 1, "qty": 1}}

        res = qc.check_condition(counts)

        assert res == 1

        qc = QtyCondition(product='Prod1', qty=1)

        counts = {"Prod1": {"price": 1, "qty": 2}}

        res = qc.check_condition(counts)

        assert res == 2

        qc = QtyCondition(product='Prod1', qty=2)

        counts = {"Prod1": {"price": 1, "qty": 0}}

        res = qc.check_condition(counts)

        assert res == 0


class TestBasket:

    def test_add_product(self):
        bsk = Basket()

        assert len(bsk.list_of_products) == 0

        bsk.add_product(product={"product":"Prod1", "price":1})

        assert len(bsk.list_of_products) == 1

        assert isinstance(bsk.list_of_products[0], Product)



    def test_count(self):
        bsk = Basket()

        bsk.add_product(product={"product": "Prod1", "price": 1})

        assert bsk.count_of_products['Prod1']['qty'] == 1

        bsk.add_product(product={"product": "Prod1", "price": 1})

        assert bsk.count_of_products['Prod1']['qty'] == 2

        assert bsk.count_of_products['Prod1']['price'] == 1