from csv import DictReader, field_size_limit
from typing import Any
from pathlib import Path

from io import Reader
import json
import csv



print(f'{'——'*20}文件写入中{'——'*20}')
data = {
    "name": "张三",
    "age": 30,
    "hobbies": ['编程', '游戏', '篮球']
}

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f'{'——'*20}文件已写入{'——'*20}')

print(f'{'——'*20}文件读取中{'——'*20}')
with open('test.json', 'r', encoding = 'utf-8') as f:
    data: dict[str, str|int|list[str]]= json.load(f)

print(f'姓名： {data['name']}')
print(f'年龄： {data['age']}')
print(f'兴趣： {data['hobbies']}')


with open('student.csv', 'w', newline = '', encoding = 'utf-8') as f:
    write = csv.writer(f)
    write.writerow(['姓名', '学号', '性别', '年龄'])
    write.writerow(['闫云祥', '24030100006', '男', '20'])
    row = [
        ['张三', '1234', '男', '24'],
        ['李四', '3456', '女', '45'],
        ['张妈', '23123', '女', '46']
    ]    
    write.writerows(row)
print('CSV文件写入完成')


with open('student.csv', 'w', newline = '', encoding = 'utf-8') as f:
    fieldnames = ['姓名', '性别', '职位', '城市']
    write = csv.DictWriter(f, fieldnames = fieldnames)

    write.writeheader()
    # 先写表头
    write.writerow({'姓名': '张三', '性别': '男', '职位': '程序员', '城市': '北京'})

    rows = [
        {'姓名': '李四', '性别': '男', '职位': '程序员', '城市': '上海'},
        {'姓名': '王五', '性别': '女', '职位': '产品经理', '城市': '深圳'},
        {'姓名': '赵六', '性别': '男', '职位': '设计师', '城市': '广州'}
    ]
    write.writerows(rows)


print(f'{'——'*20}普通reader读取{'——'*20}')
with open('student.csv', 'r', encoding = 'utf-8') as f:
    read = csv.reader(f)
    for row in read:
        print(row)

print(f'{'——'*20}字典reader读取{'——'*20}')
with open('student.csv', 'r', encoding = 'utf-8') as f:
    read = csv.DictReader(f)
    for row in read:
        print(f'{row['姓名']} | {row['性别']} | {row['职位']} | {row['城市']}')


# 一个查找CSV指定数据的方法

def query_students(csv_path: str, mid_score: int = 0, city = None) -> list[Any]:
    with open(csv_path,'r',encoding = 'utf-8') as f:
        read: DictReader[str]  =csv.DictReader(f)
        result: list[Any] = []
        for row in read:
            score: int = int(row['分数'])
            if score >= mid_score and(city is None or row['城市'] == city):
                result.append(row)
    return result 


# 一个文件扫描整理方法

def scan_directory(directory_path):
    '''扫描目录文件，按扩展名分类统计'''
    stats = {}

    for file in Path(directory_path).iterdir():
        if file.is_file():
            ext  = file.suffix.lower() or '没有扩展名'
            stats.setdefault(ext, []).append(file.name)

    # 打印统计
    print(f'目录：{directory_path}')
    print(f'{'——'*20}')
    for ext, files in stats.items():
        print(f'{ext:.<15}{len(files):>3}个文件')
        for file in files[:3]:
            print(f'[文件]:{file}')
    

scan_directory('e:/Codework')

# CSV文件向JSON文件转换

def csv_json(csv_path: str, json_path: str):
    '''将CSV文件转换为JSON文件'''
    records = []
    with open(csv_path, 'r', encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    
    Path(json_path).write_text(json.dumps(records, ensure_ascii = False, indent = 4), encoding = 'utf-8')
    print(f'CSV文件{csv_path}已转化为JSON文件{json_path}')

csv_json('student.csv', 'test.json')