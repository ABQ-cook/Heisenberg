from typing_extensions import override
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    """使用列表实现一个栈，遵循先进后出原则"""
    def __init__(self) -> None:
        self.items: list[T] = []  # 使用列表存储栈中的元素

    def is_empty(self) -> bool:
        """判断栈是否为空"""
        return len(self.items) == 0

    def push(self, item: T) -> None:
        """压栈：将元素添加到栈顶"""
        self.items.append(item)

    def pop(self) -> T:
        """弹栈：移除并返回栈顶元素，若栈为空则抛出异常"""
        if self.is_empty():
            raise IndexError("从空栈中弹出元素")
        return self.items.pop()

    def peek(self) -> T:
        """查看栈顶元素，不移除"""
        if self.is_empty():
            raise IndexError("栈为空，无法查看栈顶")
        return self.items[-1]

    def size(self) -> int:
        """返回栈中元素个数"""
        return len(self.items)

    @override
    def __str__(self) -> str:
        """方便打印栈的内容"""
        return str(self.items)


# ---------- 测试代码 ----------
if __name__ == "__main__":
    print("--- 栈测试 ---")
    stack: Stack[int] = Stack[int]()
    print('栈控制台已启动，当前可用指令为push <数字>,pop,peek,size,show,exit/quit')

    while True:
        cmd: str = input('stack> ').strip()
        if not cmd:
            continue
        parts: list[str] = cmd.split()
        action: str = parts[0].lower()
        if action == 'push':
            if len(parts) < 2:
                print('用法：push<数字>')
                continue
            try:
                stack.push(item=int(parts[1]))
            except ValueError:
                print('错误：请输入整数')
        elif action == 'pop':
            try:
                print(f'弹出元素：{stack.pop()}')
            except IndexError as e:
                print(e)
        elif action == 'peek':
            try:
                print(f'栈顶元素：{stack.peek()}')
            except IndexError as e:
                print(e)
        elif action == 'size':
            print(f'大小：{stack.size()}')
        elif action == 'show':
            print(f'{stack}')
        elif action in ('exit','quit'):
            print('bye')
            break
        else:
            print('无效命令,可用命令有:push <数字>,pop,peek,size,show,exit/quit')