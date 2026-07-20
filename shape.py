from __future__ import annotations
from abc import ABC
import math
from typing_extensions import override
from abc import abstractmethod



class Shape(ABC):
    """形状基类，包含面积和周长的属性及计算方法"""
    def __init__(self) -> None:
        self.area_val: float = 0.0
        self.perimeter_val: float = 0.0

    @abstractmethod
    def area(self) -> float: 
        """计算面积，由子类重写"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """计算周长，由子类重写"""
        pass

class Triangle(Shape):
    """三角形子类，根据三边长计算"""
    def __init__(self, a: int, b: int, c: int) -> None:
        super().__init__()
        self.a: int = a
        self.b: int = b
        self.c: int = c
    @override
    def area(self) -> float:  
        """使用海伦公式计算三角形面积"""
        s: float = (self.a + self.b + self.c) / 2
        self.area_val: float = math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
        return self.area_val
    
    @override
    def perimeter(self) -> float:
        """计算三角形周长"""
        self.perimeter_val: float = self.a + self.b + self.c
        return self.perimeter_val


class Rectangle(Shape):
    """矩形子类"""
    def __init__(self, width: float, height: float) -> None:
        super().__init__()
        self.width: float = width
        self.height: float = height

    @override
    def area(self) -> float:
        """计算矩形面积"""
        self.area_val: float = self.width * self.height
        return self.area_val

    @override
    def perimeter(self) -> float:
        """计算矩形周长"""
        self.perimeter_val: float = 2 * (self.width + self.height)
        return self.perimeter_val


class Circle(Shape):
    """圆形子类"""
    def __init__(self, radius: float) -> None:
        super().__init__()
        self.radius: float = radius

    @override
    def area(self) -> float:
        """计算圆面积"""
        self.area_val: float = math.pi * self.radius ** 2
        return self.area_val

    @override
    def perimeter(self) -> float:
        """计算圆周长"""
        self.perimeter_val: float = 2 * math.pi * self.radius
        return self.perimeter_val


if __name__ == "__main__":
    print("\n--- 形状测试 ---")
    tri: Triangle = Triangle(a=3, b=4, c=5)
    print(f"三角形(3,4,5)面积: {tri.area():.2f}, 周长: {tri.perimeter():.2f}")

    rect:Rectangle = Rectangle(width = 4, height = 6)
    print(f"矩形(4x6)面积: {rect.area():.2f}, 周长: {rect.perimeter():.2f}")

    cir: Circle = Circle(radius = 5)
    print(f"圆(r=5)面积: {cir.area():.2f}, 周长: {cir.perimeter():.2f}")