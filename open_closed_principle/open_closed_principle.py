from enum import Enum
from typing import List


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size


# --- bad way ---
class ProductFilter:
    @staticmethod
    def filter_by_color(products, color):
        for p in products:
            if p.color == color:
                yield p

    @staticmethod
    def filter_by_size(products, size):
        for p in products:
            if p.size == size:
                yield p

    @staticmethod
    def filter_by_size_and_color(products, size, color):
        for p in products:
            if p.color == color and p.size == size:
                yield p


# OCP == open for extension, closed for modification
# Specification
class Specification:
    def is_satisfied(self, item: Product) -> bool:
        pass

    def __and__(self, other):
        return AndSpecification(self, other)


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item: Product) -> bool:
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args
        ))


class Filter:
    def filter(self, items: List[Product], spec: Specification) -> List[Product]:
        pass


class ColorSpecification(Specification):
    def __init__(self, color: Color):
        self.color = color

    def is_satisfied(self, item: Product):
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size: Size):
        self.size = size

    def is_satisfied(self, item: Product):
        return item.size == self.size


class BetterFilter(Filter):
    def filter(self, items: List[Product], spec: Specification):
        for item in items:
            if spec.is_satisfied(item):
                yield item


if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('Blue', Color.BLUE, Size.LARGE)

    products = [apple, tree, house]
    pf = ProductFilter()
    print("Green products (old):")
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f' - {p.name} is green')

    bf = BetterFilter()
    print("Green products (new):")
    green = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green):
        print(f' - {p.name} is green')

    print("Large products:")
    large = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large):
        print(f' - {p.name} is large')

    print("Large blue items:")
    # large_blue = AndSpecification(large,
    #                               ColorSpecification(Color.BLUE))
    large_blue = large & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is large and blue')
