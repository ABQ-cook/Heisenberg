from typing import Any, Callable, Protocol, TypeVar

class SupportsLessThan(Protocol):
    """支持 < 比较的协议类型。"""

    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar('T', bound=SupportsLessThan)  # 泛型类型变量，约束 T 必须支持 < 比较


def merge(left: list[T], right: list[T]) -> list[T]:
    result: list[T] = []
    i = j = 0
    while(i < len(left) and j < len(right)):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])         
    return result

def sort_divide(arr: list[T]) -> list[T]:
    if len(arr)<=1:
        return arr
    mid: int = (len(arr))//2
    left: list[T] = sort_divide(arr[:mid])
    right: list[T] = sort_divide(arr[mid:])
    return merge(left,right)

def mysort(nums: list[int], *, key: Callable[[int], Any] | None = None, reverse: bool = False) -> list[int]: #"*"表示后面的参数必须以关键字的形式传入
    number: list[int] = list[int](nums)
    if len(number) <= 1:
        return number
    if key is not None:
        decorated: list[tuple[Any,int]] = [(key(item),item) for item in number]
        decorated: list[tuple[Any,int]] = sort_divide(decorated)
        sort_number: list[int] = [item for _,item in decorated] #“_”是一个占位符，表示我们不关心这个值
    else:
        sort_number: list[int] = sort_divide(number)
    if reverse:
        sort_number.reverse()
    return sort_number

def main() -> None:
    print(mysort(nums = [3,-4,6,1,2,-8,10],reverse = False))
    y: list[int]= [3,-4,6,1,2,-8,10]
    print(mysort(nums = y, key=abs,reverse = False))

if __name__ == "__main__":
    main()
