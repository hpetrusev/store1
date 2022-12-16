from format_number_representation import PoundFormatter


class TestFormatter:
    def test_full_formatter(self):
        pf = PoundFormatter()

        formatted = pf.format_number(100)
        assert formatted == "£100.00"

        formatted = pf.format_number(100.1)
        assert formatted == "£100.10"

        formatted = pf.format_number(100.1111)
        assert formatted == "£100.11"

    def test_penny_output(self):
        pf = PoundFormatter()

        formatted = pf.format_number(0.1)
        assert formatted == "10p"

        formatted = pf.format_number(0.15)
        assert formatted == "15p"

        formatted = pf.format_number(0.1111111)
        assert formatted == "11p"
