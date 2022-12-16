from db_ops import JsonDatabase, Filtering


class TestJsonDatabase:
    def test_read_price(self):
        db = JsonDatabase()

        price_data = db.get("prices")

        assert isinstance(price_data, list)

    def test_read_offers(self):
        db = JsonDatabase()

        price_data = db.get("offers")

        assert isinstance(price_data, list)

    def test_filter_single(self):
        db = JsonDatabase()
        object_asking = "Apples"

        filter_n = Filtering(filter_by="product", filter_value=[object_asking])

        price_data = db.get("prices", [filter_n])

        element = price_data[0]

        value = element["product"]

        assert value == object_asking

    def test_filter_multiple(self):
        db = JsonDatabase()
        object_asking = "Apples"
        value_filter = 0.1

        filter_n = Filtering(filter_by="product", filter_value=[object_asking])

        filter_n1 = Filtering(filter_by="discount", filter_value=[value_filter])

        price_data = db.get("offers", [filter_n, filter_n1])

        assert isinstance(price_data, list)

        element = price_data[0]

        assert element["product"] == object_asking

        assert element["discount"] == value_filter
