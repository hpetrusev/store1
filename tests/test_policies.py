from policies import CalcController, PriceBasketPolicy
from calculators import ProductSumCalculator


class TestCalcController:
    def test_get_calc(self):
        cc = CalcController(calculators_needed=['ProductSumCalculator'])
        assert isinstance(cc.calculators['ProductSumCalculator'], ProductSumCalculator)


class TestPriceBasketPolicy:
    valid_items = ['Prod1', 'Prod2', 'Prod3']
    invalid_items = ['Prod4', 'Prod5']

    def test_step_one_get_obj_into_basket(self):
        # test get items into basket, that are valid

        pbp = PriceBasketPolicy()
        pbp._db.data['prices'] = [{"product": a, "price": 1} for a in self.valid_items]

        pbp.get_objects_into_basket(self.valid_items)

        assert [a.name for a in pbp.basket.list_of_products] == self.valid_items

        # test not getting items into basket

        pbp.get_objects_into_basket(self.invalid_items)

        assert all([a not in [a.name for a in pbp.basket.list_of_products] for a in self.invalid_items])

    def test_initiate_calc_controller(self):

        pbp = PriceBasketPolicy()

        pbp._db.data['prices'] = [{"product": a, "price": 1} for a in self.valid_items]
        pbp._db.data['offers'] = [{"product": self.valid_items[0], "discount": 0.1,
                                   "condition": [], "applies": -1, "active": True, "message": "10% off"}]
        pbp.initiate_calc_controller()

        # assert calc applier is created

        assert pbp.calc_applier is not None

        # assert the offers are getting passed

        assert pbp.calc_applier.calculators['OfferCalculator'].offers[0].product == self.valid_items[0]
        assert pbp.calc_applier.calculators['OfferCalculator'].offers[0].message == '10% off'


    def test_step_two_apply_calculations(self):

        # no valid offers calcs

        pbp = PriceBasketPolicy()

        pbp._db.data['prices'] = [{"product": a, "price": 1} for a in self.valid_items]
        pbp._db.data['offers'] = []

        pbp.initiate_calc_controller()

        pbp.get_objects_into_basket(self.valid_items)

        total, subtotal, per_offer = pbp.apply_calculations()

        assert total == 3
        assert subtotal == 3
        assert len(per_offer) == 0

        # with valid offers calcs

        pbp = PriceBasketPolicy()

        pbp._db.data['prices'] = [{"product": a, "price": 1} for a in self.valid_items]
        pbp._db.data['offers'] = [{"product":self.valid_items[0],  "discount": 0.1,
                                   "condition": [], "applies": -1, "active":  True, "message":  "10% off"}]

        pbp.initiate_calc_controller()

        pbp.get_objects_into_basket(self.valid_items)

        total, subtotal, per_offer = pbp.apply_calculations()

        assert total == 2.9
        assert subtotal == 3
        assert len(per_offer) == 1
        assert per_offer[0][1] == 0.1
        assert per_offer[0][0] == '10% off'
