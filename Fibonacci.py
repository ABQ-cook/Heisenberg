class Fibonacci():
    def __init__(self) -> None:
        self.prev : int = 0
        self.curr : int = 1

    def __iter__(self) -> Fibonacci:
        return self
    
    def __next__(self) -> int:
        value: int = self.curr
        self.curr += self.prev
        self.prev = value
        return value
