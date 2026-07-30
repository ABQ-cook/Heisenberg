# Class类

## 一、 Class类基本方法

必须方法：

1. 初始化 `__init__` 

每个类对象必须包含的一个方法，用于初始化实例变量，在创建实例时自动调用

魔法方法：为类对象赋予一定的能力

1. 对象表示 `__repr__` 和 `__str__` 

决定你的类如何表现出来：

 `__repr__` 在交互式环境下查看变量- `repr(obj)`

 `__str__` 决定 `print(obj)\str(obj)` 如何输出示例内容

```python
class Person:
def **repr**(self):
return f"Person(name={[self.name](http://self.name/)!r}, age={self.age!r})"
def **str**(self):
return f"{[self.name](http://self.name/)}({self.age}岁)"

p = Person("Alice", 25)
p          # Person(name='Alice', age=25)  ← 调 **repr**
print(p)   # Alice(25岁)      
```

1. 相等比较 `__eq__` 

```python
class Person:
def **eq**(self, other):
if not isinstance(other, Person):
return NotImplemented
return [self.name](http://self.name/) == [other.name](http://other.name/) and self.age == other.age

p1 = Person("Alice", 25)
p2 = Person("Alice", 25)
p1 == p2
有 **eq**：True ✓（比较内容）
无 **eq**：False ✗（比较内存地址）
```

1. 哈希化 `__hash__` 

让你的类对象变得可哈希，以便于将其作为字典的key

```python
class Person:
def **hash**(self):
return hash(([self.name](http://self.name/), self.age))

有了 **hash**，实例可作为 dict key 或 set 元素
d = {p: "info"}       # ✅
s = {p1, p2}          # ✅ 去重
```

一个完整的类定义：

```python
class Student:
def **init**(self, name: str, score: int = 0):
[self.name](http://self.name/) = name
self.score = score

def __repr__(self):
    return f"Student(name={self.name!r}, score={self.score!r})"

def __eq__(self, other):
    if not isinstance(other, Student):
        return NotImplemented
    return (self.name, self.score) == (other.name, other.score)

def __hash__(self):
    return hash((self.name, self.score))

def __lt__(self, other):
    return self.score < other.score
```

## 二、 `dataclass` 数据类简化定义方法

只需描述数据（此处称为字段），自动生成 `__init__、__repr__、__eq__` 等方法

1. `dataclass`有以下常见参数：

```python
@dataclass(
init=True,          # 自动生成 **init**
repr=True,          # 自动生成 **repr**
eq=True,            # 自动生成 **eq**
order=False,        # 生成 **lt**/**le**/**gt**/**ge**
frozen=False,       # 实例不可变（类似 NamedTuple）
unsafe_hash=False,  # 强制生成 **hash**
kw_only=False,      # 强制关键字传参（3.10+）
slots=False,        # 使用 **slots** 节省内存（3.10+）
)
```

1. `field()` 用于精细控制每个字段（数据变量）

[`field()`用法详解](Class%E7%B1%BB/field()%E7%94%A8%E6%B3%95%E8%AF%A6%E8%A7%A3%203ab19b7afce98043bca8dd4131d2248f.md)

1. 有 `__post_init__` 方法，会在每次 `__init__` 被调用后调用

```python
@dataclass
class Vector:
    x: float
    y: float

def magnitude(self) -> float:           # ← 普通方法
    return (self.x**2 + self.y**2) ** 0.5

def __post_init__(self):                # ← __init__ 后自动调用
    if self.x == 0 and self.y == 0:
        raise ValueError("不允许零向量")
        
v = Vector(3.0, 4.0)
v.magnitude()  # 5.0

Vector(0.0, 0.0)  # ❌ ValueError: 不允许零向量
```