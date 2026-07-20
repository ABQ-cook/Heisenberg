def outer(m):
    print(f'外部参数：{m}')
    def inner(n):
        print(f'内部参数：{n}')
        return m+n
    return inner 

ot = outer(10)
print(f'ot(10):{ot(10)}')
print(f'ot(20):{ot(20)}')
