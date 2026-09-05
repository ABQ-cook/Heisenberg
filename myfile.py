from typing import Any


class Myfile:
    '''文件上下文管理器'''
    def __init__(self,filename: str,  mode: str)  -> None:
        self.filename: str = filename
        self.mode: str= mode
        self.file: Any =  None

    def __enter__(self) -> Any:
        '''进入with块后执行，将返回值赋给as后的变量'''
        print(f'[打开文件]:{self.filename}')
        self.file = open(self.filename, self.mode)
        return self.file

    def  __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        '''离开with块后执行'''
        print(f'[关闭文件]：{self.filename}')
        if self.file:
            _ = self.file.close()
        return False


from contextlib import contextmanager

@contextmanager
def myfile(filename: str, mode: str):
    print(f'打开文件：{filename}')
    f = open(filename, mode)
    try:
        yield f           # 将上下内容一分为二，上面是进入with块后执行，下面是离开with块后执行
    finally:
        print(f'关闭文件: {filename}')
        f.close()

