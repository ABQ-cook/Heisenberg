def sum_all(*args:int) -> int:
    total: int = 0  
    for num in args:
        total = total + num
    return total

user_input: str = input("请输入任意个数数字，用空格分隔")
str_input: list[str] = user_input.split()
int_input: list[int] = [int(num) for num in str_input]

maxsum: int = max(int_input)

print(f"最大的数字是：{maxsum}，所有数字的和是:{sum_all(*int_input)}")
