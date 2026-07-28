from typing import Callable, ParamSpec, TypeVar, Generic
from functools import wraps, update_wrapper
import time
from collections import OrderedDict

# 1. 日志装饰器
P = ParamSpec('P')
R = TypeVar('R')

def log(fn: Callable[P, R]) -> Callable[P, R]: #表示log装饰器接收任意签名的可调用对象，并返回一个可调用对象
    '''简单的日志装饰器'''
    @wraps(fn)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R: 
        print(f'{'='*30}日志装饰器作用开始{'='*30}')
        print(f'[LOG]函数{fn.__name__}即将被调用')
        # 下面这样的try方法结构更加健壮
        try:
            res = fn(*args, **kwargs)
            print(f'[LOG]函数{fn.__name__}调用完毕，返回值为{res}')
            print(f'{'='*30}日志装饰器作用结束{'='*30}')
            return res
        except Exception as e:
            print(f'[LOG]函数调用失败，抛出异常：{e!r}')
            print(f'{'='*30}日志装饰器作用结束{'='*30}')
            raise
    return inner

# 2. 计时装饰器

def timer(fn: Callable[P, R]) -> Callable[P, R]:
    '''简易计时装饰器,单位为毫秒ms'''
    
    @wraps(wrapped=fn)
    def inner(*args:P.args, **kwargs:P.kwargs) -> R:
        print(f'{'='*30}计时装饰器作用开始{'='*30}')
        start_time: float = time.perf_counter()
        res = fn(*args, **kwargs)
        end_time: float = time.perf_counter()
        elapsed: float = end_time - start_time
        print(f'函数{fn.__name__}执行耗时{elapsed*1000:.4f}ms')
        print(f'{'='*30}计时装饰器作用结束{'='*30}')
        return res
    return inner

# 3. 重试装饰器（工厂模式）

def retry(times: int = 5, delay: float = 0.0, backoff: float = 1.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """重试装饰器工厂

    :param times:  最大重试次数
    :param delay:  初始等待秒数
    :param backoff: 退避倍数，每次重试后 delay *= backoff
    """
    if times < 1:
        raise ValueError(f'times 必须 >= 1，当前为 {times}')

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay: float = delay
            last_exc: Exception | None = None
            for i in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f'函数 {fn.__name__} 调用失败，第 {i+1}/{times} 次重试中...')
                    time.sleep(current_delay)
                    current_delay *= backoff
            # 重抛最后一个异常，保留原始堆栈信息
            raise RuntimeError(
                f'函数 {fn.__name__} 在 {times} 次重试后仍失败'
            ) from last_exc
        return inner
    return decorator

# 4. 缓存参数（cache）装饰器

def cache(fn: Callable[P,R]) -> Callable[P, R]:
    '''参数缓存装饰器，使用Lru_cache实现，将需要的参数缓存起来，下次调用时，如果参数相同，则直接返回缓存的结果'''
    _cache: dict[tuple[object,...], R] = {}

    @wraps(wrapped = fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # kwargs是dict类型，不可哈希，无法作为字典key值，需要使用frozenset来转换为可哈希对象
        key: tuple[object, ...] = (args, frozenset(kwargs.items()))
        if key not in _cache:
            _cache[key] = fn(*args, **kwargs)
        return _cache[key]
    
    return wrapper

# 5. 进阶版cache装饰器，使用了Lru_cache来实现，在cache达到最大值的时候，会依据lru算法删除最不常用的缓存

class _LruCacheWrapper(Generic[P, R]):
    '''LRU 缓存包装器：可调用对象，同时暴露 cache_info / cache_clear'''
    fn: Callable[P, R]
    maxsize: int
    _cache: OrderedDict[tuple[tuple[object, ...], frozenset[tuple[str, object]]], R]
    hits: int
    misses: int

    def __init__(self, fn: Callable[P, R], maxsize: int) -> None:
        _ = update_wrapper(self, fn)
        self.fn = fn
        self.maxsize = maxsize
        self._cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        '''将包装函数的内容放入__call__方法中，让该实例对象变得可调用'''
        key: tuple[tuple[object, ...], frozenset[tuple[str, object]]] = (args, frozenset(kwargs.items()))

        # 缓存命中，将该key移动到末尾，标记为最近使用
        if key in self._cache:
            self.hits += 1
            self._cache.move_to_end(key)
            return self._cache[key]

        # 缓存未命中，调用函数计算结果并存入缓存
        self.misses += 1
        res: R = self.fn(*args, **kwargs)
        self._cache[key] = res

        # 超出容量时，弹出最左边（最久未使用）的缓存
        if len(self._cache) > self.maxsize:
            _ = self._cache.popitem(last=False)
        return res

    def cache_info(self) -> dict[str, object]:
        '''暴露缓存信息用于调试'''
        return {
            'hits': self.hits,
            'misses': self.misses,
            'currsize': len(self._cache),
            'maxsize': self.maxsize,
        }

    def cache_clear(self) -> None:
        '''清空缓存并重置统计'''
        self._cache.clear()
        self.hits = 0
        self.misses = 0


def Lru_cache(maxsize: int = 128) -> Callable[[Callable[P, R]], _LruCacheWrapper[P, R]]:
    '''依据LRU算法实现的缓存装饰器，在缓存达到最大值的时候，会删除最不常用的缓存'''
    if maxsize < 1:
        raise ValueError(f'maxsize 必须 >= 1, 当前为{maxsize}')

    def decorator(fn: Callable[P, R]) -> _LruCacheWrapper[P, R]:
        return _LruCacheWrapper(fn, maxsize)
    return decorator






# --- Lru_cache 装饰器测试 ---
@Lru_cache(maxsize=64)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

_ = fib(10)  # type: ignore[reportUnusedCallResult]
print(fib.cache_info())     # 查看：命中次数、未命中次数、缓存大小、容量上限
fib.cache_clear()           # 清空缓存并重置统计
print(fib.cache_info())     # 清空后统计应全部归零




@retry(times=3, delay=0.5, backoff=2.0)
@timer
@log
def add(x: int, y: int) -> int:
    '''两个整数相加'''
    return x + y

_ = add(1,2)
print(add.__name__)
print(add.__doc__)