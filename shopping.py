from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    _price: float
    _stock: int = field(default=0)

    def __post_init__(self) -> None:
        self.price = self._price
        self.stock = self._stock

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            raise ValueError('价格必须大于0')
        self._price = value
    
    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int) -> None:
        if value < 0:
            raise ValueError('库存必须大于等于0')
        self._stock = value
    



    # TODO: 用 property 校验 price > 0、stock >= 0

@dataclass
class Cart:
    items: dict[Product, int] = field(default_factory=dict)   # 商品 -> 数量

    @property
    def total_price(self) -> float:
        # TODO: 返回购物车总价（只读，不能赋值）
        ...