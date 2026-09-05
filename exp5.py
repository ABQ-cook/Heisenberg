import time
from turtle import end_fill
from typing import Callable, ParamSpec, TypeVar, Generic
from functools import wraps


P = ParamSpec('P')
R = TypeVar('R')

def timer(fn: Callable[P, R]) -> Callable[P, R]:
    '''简易计时器'''
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time: float = time.perf_counter()
        res: R = fn(*args, **kwargs)
        end_time: float = time.perf_counter()
        elapsed: float = end_time - start_time
        print(f'函数{fn.__name__}执行耗时{elapsed*1000:.4f}ms')
        return  res
    return wrapper
