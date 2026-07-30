# Collections 模块

一、  `OrderedDict` ：一种带有特殊方法的有序字典，有两个常用方法：

1.  `move_to_end(key=..., last=True)` ：表示将指定的 `key` 移动到字典的某一端

`last = True（默认）` 表示将key移动到末尾

`last = False` 表示将key移动到开头

```python
d = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
d.move_to_end('a')      # a 被移到最后
print(list(d.keys()))   # ['b', 'c', 'a']
```

1. `popitem(last=True)` ：表示弹出某一端的 `key` 

`last = True（默认）` 表示弹出末尾的 `key` 

`last = False` 表示弹出开头的 `key` 

```python
d = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
k, v = d.popitem(last=False)  # 弹出最旧的 'a'
print(k, v)  # a 1
print(list(d.keys()))  # ['b', 'c']
```