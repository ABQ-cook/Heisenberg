import math
from collections.abc import Generator  


def is_prime(n: int) -> bool:
    """判断一个数是否为质数（素数）"""
    if n <= 1:
        return False
    # 检查从 2 到 sqrt(n) 的整数是否能整除 n
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_generator(start: int, end: int) -> Generator[int, None, None]:
    """生成器，逐个产生 [start, end] 范围内的质数"""
    # 质数最小为 2，因此从 max(2, start) 开始
    for num in range(max(2, start), end + 1):
        if is_prime(num):
            yield num

def sum_of_primes(start: int, end: int) -> int:
    """返回起止范围内所有质数的和"""
    return sum(prime_generator(start, end))

# 示例使用
if __name__ == "__main__":
    start : int = 10
    end : int = 50
    total : int = sum_of_primes(start, end)
    print(f"{start} 到 {end} 之间的质数和为: {total}")
    # 可以输出质数列表以供验证
    print("质数列表:", list[int](prime_generator(start, end)))