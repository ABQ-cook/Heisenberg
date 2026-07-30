# field()用法详解

## `field()` 参数详解

`field()` 来自 `dataclasses` 模块，用于**精细控制数据类中每个字段的行为**。它的完整签名如下：

```python
def field(
    *,
    default: Any = MISSING,           # 默认值
    default_factory: Callable[[], Any] = MISSING,  # 默认值工厂函数
    init: bool = True,                # 是否出现在 __init__ 中
    repr: bool = True,                # 是否出现在 __repr__ 中
    hash: Optional[bool] = None,      # 是否参与 __hash__ 计算
    compare: bool = True,             # 是否参与 __eq__ / __lt__ 等比较
    metadata: Optional[Mapping] = None, # 附加元数据
    kw_only: bool = MISSING,          # 是否强制关键字传参（3.10+）
)
```

> **注意**：所有参数都是关键字参数，必须用 `field(key=value)` 的形式，不能按位置传。
> 

---

### 1. `default` — 默认值

为字段提供默认值，使其成为可选参数：

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str                    # 必填，无默认值
    age: int = 18                # 方法一：直接用 "= 值"（等价写法）
    level: int = field(default=1)  # 方法二：用 field(default=...)

User("Alice")           # User(name='Alice', age=18, level=1)
User("Bob", 25, 3)      # User(name='Bob', age=25, level=3)
```

> **规则**：`= 值` 和 `field(default=值)` 等价，但**可变默认值必须用 `field(default_factory=...)` 而不是 `field(default=...)`**。
> 

---

### 2. `default_factory` — 默认值工厂函数（关键参数）

用于为**可变类型**（`list`、`dict`、`set`）提供默认值，每次实例化都调用一次工厂函数，确保每个实例获得**独立的新对象**。

```python
@dataclass
class Team:
    # ❌ 危险：所有实例共享同一个 list！（手写 __init__ 里也会犯这个错）
    # members: list[str] = []

    # ✅ 正确：每次实例化都创建一个新 list
    members: list[str] = field(default_factory=list)

    # ✅ 带初始元素的 list
    tags: list[str] = field(default_factory=lambda: ["new"])

    # ✅ 空 dict
    config: dict[str, str] = field(default_factory=dict)

    # ✅ 当前时间（每次实例化取最新时间）
    created_at: float = field(default_factory=lambda: __import__("time").time())

t1 = Team()
t2 = Team()
t1.members.append("Alice")
print(t1.members)  # ['Alice']
print(t2.members)  # []  ← 互不影响！
```

**为什么可变默认值要这样做？**

```python
# 问题的本质（手写 __init__ 也一样）
def __init__(self, members=[]):   # [] 在函数定义时只创建一次！
    self.members = members

# field(default=[]) 相当于上面的错误写法
# field(default_factory=list) 相当于
def __init__(self, members=None):
    self.members = members if members is not None else []  # 每次调用都新建
```

主要原因是写在 `__init__` 函数签名里的 `members=[]` 会在解释器扫描到类定义里时就定义一个空列表出来，如果后续直接调用该函数而不重新在 `__init__` 内部通过代码为新实例创建新列表的话，后续的若干个实例就会共用这个最早创建的旧列表。

如果像上面代码示例的第二个代码块那样，优化了函数签名并在 `__init__` 内部通过代码

 `self.members = members if members is not None else []` 

重新为每个新实例创建新的列表，就会避免上面那种共用情况出现。

**`default` 和 `default_factory` 互斥**，不能同时使用：

```python
field(default=0, default_factory=int)  # ❌ ValueError!
```

---

### 3. `init` — 是否作为构造参数

简单理解来说，就是若对某个字段赋值 `init = false` ，则该字段无法通过构造函数传入赋值

而若 `init = True` （默认），则该字段可通过构造函数传入赋值

```python
@dataclass
class Order:
    id: str
    amount: float
    _total: float = field(default=0.0, init=False)  # 不能从构造函数传入

    def __post_init__(self):
        self._total = self.amount * self.tax_rate  # 内部计算，不需要外部传

o = Order("A001", 100.0)
print(o)  # Order(id='A001', amount=100.0, _total=0.0)

o = Order("A001", 100.0, 999.0)  # ❌ TypeError: got unexpected keyword
```

典型场景：**派生值**、**缓存值**、**内部状态**只需要计算结果，不需要用户传入。

---

### 4. `repr` — 是否出现在 `__repr__` 中

只能修改 `__repr__` ，控制某些字段不在 `repr` 的调用中显示。

如果要同步修改 `__str__` 的显示，则要重新手写 `__str__` 方法，屏蔽某些字段的显示。

```python
@dataclass
class User:
    username: str
    password: str = field(repr=False)     # 密码不打印
    api_key: str = field(repr=False)      # 敏感信息不暴露
    email: str = ""

u = User("alice", "secret123", "sk-abc")
print(u)  # User(username='alice', email='')

# 在日志中打印时不会泄露敏感信息
import logging
logging.info("用户登录：%r", u)  # 安全
```

---

### 5. `hash` — 控制哈希行为

```python
# 场景一：某字段不参与哈希
@dataclass(unsafe_hash=True)  # 手动启用哈希
class Person:
    name: str
    age: int
    temp_id: str = field(hash=False)  # 临时 ID，不参与哈希

p1 = Person("Alice", 25, "tmp001")
p2 = Person("Alice", 25, "tmp002")
hash(p1) == hash(p2)  # True

# 场景二：从哈希中排除不可哈希的字段
@dataclass(unsafe_hash=True)
class Config:
    name: str
    data: dict = field(default_factory=dict, hash=False)  # dict 不可哈希，必须排除
```

| `hash` 值 | 含义 |
| --- | --- |
| `None`（默认） | 继承类的 `__hash__` 自动生成逻辑 |
| `True` | 参与 `__hash__` 计算 |
| `False` | 不参与 `__hash__` 计算 |

---

### 6. `compare` — 是否参与比较

```python
@dataclass(order=True)  # 同时启用等值和大小比较
class Student:
    name: str = field(compare=False)  # 只按成绩，姓名不参与比较
    score: int = 0
    id: str = field(compare=False)    # ID 也不参与

s1 = Student("Alice", 90, "001")
s2 = Student("Bob", 90, "002")

s1 == s2            # True（只看 score）

@dataclass
class Product:
    name: str
    price: float
    cache_key: str = field(compare=False)  # 只比较商品内容，缓存键不参与

p1 = Product("Book", 29.9, "ck-001")
p2 = Product("Book", 29.9, "ck-002")
p1 == p2  # True
```

**典型场景**：同一个人的两份记录，只有内存 ID 不同，实际数据相同。用 `compare=False` 排除无关字段。

---

### 7. `metadata` — 附加元数据

不影响类行为，纯粹是**贴在字段上的标签**，供外部框架（如序列化、ORM、表单验证）使用：

```python
@dataclass
class User:
    name: str = field(metadata={"help": "用户名", "max_length": 20})
    age: int = field(metadata={"help": "年龄", "min": 0, "max": 150})

# 通过 fields() 函数读取
from dataclasses import fields

for f in fields(User):
    print(f"{f.name}: {f.metadata}")
# name: {'help': '用户名', 'max_length': 20}
# age: {'help': '年龄', 'min': 0, 'max': 150}
```

**典型场景**：

- REST API 框架（如 FastAPI）用于定义字段验证规则
- ORM（如 SQLAlchemy）用于映射数据库列属性
- 序列化库用于控制字段名转换

---

### 8. `kw_only` — 强制关键字传参（3.10+）

`kw_only = True` 表示该字段的赋值只能通过关键字显式一一对应传入

```python
@dataclass
class Rectangle:
    width: float
    height: float
    name: str = field(default="矩形", kw_only=True)      # 必须用关键字传
    color: str = field(default="white", kw_only=True)

r = Rectangle(10.0, 20.0, name="画布1", color="red")    # ✅
r = Rectangle(10.0, 20.0, "画布1", "red")               # ❌ TypeError

# 类级别设置 kw_only=True 等价于每个字段都设 kw_only
@dataclass(kw_only=True)
class AllKW:
    a: int
    b: int = 5
```

适用场景：字段含义不直观、参数众多时，强制用关键字提高可读性。

---

### 9. `field()` 参数组合示例

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(order=True)
class BlogPost:
    title: str                                           # 必填 + 参与排序
    content: str = field(repr=False, compare=False)       # 内容太长，不打印不参与比较
    author: str = field(default="匿名", compare=False)     # 默认值 + 不参与排序
    tags: list[str] = field(default_factory=list,        # 可变默认 + 不参与哈希
                             hash=False, compare=False)
    created_at: datetime = field(default_factory=datetime.now,  # 每次新建都用当前时间
                                   repr=True, compare=True)
    view_count: int = field(default=0, init=False,       # 内部计数器，不能外部传入
                             compare=True)
    slug: str = field(init=False)                        # 不传也不设默认值，需在 __post_init__ 中赋值

    def __post_init__(self):
        self.slug = self.title.lower().replace(" ", "-")  # 自动生成 slug

# 使用
post = BlogPost("Hello World", "很长的文章内容...", tags=["python", "dataclass"])
print(post)
# BlogPost(title='Hello World', tags=['python', 'dataclass'],
#          created_at=datetime(...), view_count=0, slug='hello-world', ...)
```

---

### 快速查阅表

| 参数 | 默认值 | 作用 | 典型场景 |
| --- | --- | --- | --- |
| `default` | `MISSING` | 默认值 | 普通默认值 |
| `default_factory` | `MISSING` | 默认值工厂 | `list`/`dict`/`set` 等可变默认值 |
| `init` | `True` | 是否构造参数 | 派生字段、内部状态 |
| `repr` | `True` | 是否打印显示 | 密码、token、大文本 |
| `hash` | `None` | 是否参与哈希 | 排除 `unhashable` 字段（如 `dict`） |
| `compare` | `True` | 是否参与比较 | 排除无关字段，避免错误去重 |
| `metadata` | `None` | 附加元信息 | 框架集成（校验、序列化、ORM） |
| `kw_only` | `MISSING` | 强制关键字 | 参数多时提高可读性 |