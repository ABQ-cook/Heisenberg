from typing import override
from dataclasses import dataclass



class Book:
    def __init__(self, title: str, author: str, price: float, year: int):
        self.title: str = title
        self.author: str = author
        self.price: float = price
        self.year: int = year

    @override
    def __repr__(self) -> str:
        return f'title: {self.title}, author: {self.author}, price: {self.price}, year: {self.year}'
    
    @override
    def __eq__(self, other: object) -> bool:  
        if not isinstance(other, Book):
            return NotImplemented
        return self.title == other.title and self.author == other.author and self.price == other.price and self.year == other.year


'''
@dataclass
class Book:
    title: str
    author: str
    price: float
    year: int
'''


b1 = Book("三体", "刘慈欣", 39.0, 2008)
b2 = Book("三体", "刘慈欣", 39.0, 2008)
print(b1 == b2)   # 应为 True
print(b1)         # 应显示书名/作者等，而不是 <__main__.Book object at ...>


class Temmperature:
    _celsius: float = 0.0
    def __init__(self, celsius:float = 0.0) -> None:
        self.celsius = celsius    #如此赋值可保证构造时也走setter检验数值

    
    @property
    def celsius(self) -> float:
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value <  -273.15:
            raise ValueError('温度不能低于绝对零度 -273.15度')
        self._celsius = value


    @property
    def fahrenheit(self) -> float:
        return (self._celsius * 9 / 5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self._celsius = (value - 32) * 5 / 9


