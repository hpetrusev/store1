from abc import abstractmethod


class Formatter:
    @abstractmethod
    def format_number(self, number):
        pass


class PoundFormatter(Formatter):
    def format_number(self, number):
        if number < 1:
            number = round(number, 2)
            number = int(number * 100)
            return f"{number}p"
        else:
            return f"£{number:.2f}"


def get_formatter(formatter_name):
    formatters = {"PoundFormatter": PoundFormatter}
    return formatters[formatter_name]()
