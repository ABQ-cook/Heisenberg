# JSON、CSV、pathlib 学习讲义

> 对应学习计划：Week 1 Day 5 — 周一 7/27：文件 I/O + 综合实战
> 
> 学习目标：掌握 Python 三大文件处理利器，完成文件自动分类器 CLI + JSON 版通讯录

---

## 目录

- [第一部分：JSON 模块](#第一部分json-模块)
- [第二部分：CSV 模块](#第二部分csv-模块)
- [第三部分：pathlib 模块](#第三部分pathlib-模块)
- [第四部分：三种工具的对比与选择](#第四部分三种工具的对比与选择)
- [第五部分：综合实战演练](#第五部分综合实战演练)
- [第六部分：自测练习](#第六部分自测练习)

---

## 第一部分：JSON 模块

### 1.1 什么是 JSON？

**JSON**（JavaScript Object Notation）是一种轻量级的**数据交换格式**，是目前 Web 开发中最通用的数据传输格式。

```json
{
  "name": "张三",
  "age": 25,
  "skills": ["Python", "FastAPI"],
  "address": {
    "city": "北京",
    "district": "海淀"
  },
  "is_student": true,
  "graduation_year": null
}
```

**特点**：
- 纯文本，人类可读
- 与编程语言无关（几乎所有语言都支持）
- 结构清晰，支持嵌套（对象套对象、数组套对象等）

### 1.2 Python ↔ JSON 类型对照表

| Python 类型 | JSON 类型 | 说明 |
|------------|----------|------|
| `dict` | `object` | 键必须是字符串 |
| `list` / `tuple` | `array` | tuple 编码后变 array，解码回来是 list |
| `str` | `string` | JSON 必须用双引号 |
| `int` / `float` | `number` | 不支持 `Decimal`、复数等 |
| `True` / `False` | `true` / `false` | 注意 JSON 是小写 |
| `None` | `null` | 注意 JSON 中是 `null` |

> ⚠️ **易错点**：Python 的 `datetime`、`set`、自定义类对象不能直接序列化，需要手动转换。

### 1.3 核心四个函数

```python
import json
```

| 函数 | 方向 | 说明 |
|------|------|------|
| `json.dumps(obj)` | Python → JSON字符串 | 序列化，返回字符串 |
| `json.dump(obj, f)` | Python → JSON文件 | 序列化，直接写入文件对象 |
| `json.loads(s)` | JSON字符串 → Python | 反序列化，从字符串解析 |
| `json.load(f)` | JSON文件 → Python | 反序列化，从文件对象读取 |

**记忆口诀**：带 `s` 的（dumps / loads）操作**字符串**，不带的（dump / load）操作**文件**。

### 1.4 基础操作

#### 写入 JSON：`json.dump()`

```python
import json

data = {
    "name": "张三",
    "age": 25,
    "hobbies": ["编程", "游戏", "篮球"]
}

# 写入文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("数据已写入 data.json")
```

#### 读取 JSON：`json.load()`

```python
import json

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data["name"])      # 张三
print(data["hobbies"])   # ['编程', '游戏', '篮球']
```

#### 字符串 ↔ 字典：`dumps()` 与 `loads()`

```python
import json

# Python 对象 → JSON 字符串
person = {"name": "李四", "score": 95}
json_str = json.dumps(person, ensure_ascii=False)
print(json_str)          # {"name": "李四", "score": 95}
print(type(json_str))    # <class 'str'>

# JSON 字符串 → Python 对象
parsed = json.loads('{"name": "王五", "score": 88}')
print(parsed["name"])    # 王五
print(type(parsed))      # <class 'dict'>
```

### 1.5 关键参数详解

| 参数 | 作用 | 示例 |
|------|------|------|
| `indent=4` | 缩进美化输出 | 不加则所有内容在一行 |
| `ensure_ascii=False` | 允许输出中文 | **默认 True 会将中文转成 Unicode 转义** |
| `sort_keys=True` | 按键名字母排序 | 方便版本对比 |
| `separators` | 自定义分隔符 | `(",", ":")` 可压缩体积 |

```python
# 美化输出 vs 压缩输出
data = {"name": "张三", "age": 25}

# 美化输出
print(json.dumps(data, ensure_ascii=False, indent=4))
# {
#     "name": "张三",
#     "age": 25
# }

# 压缩输出
print(json.dumps(data, ensure_ascii=False))
# {"name": "张三", "age": 25}
```

### 1.6 处理复杂类型

```python
from datetime import datetime

# 自定义编码器
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)

data = {
    "user": "admin",
    "login_time": datetime.now()
}

# 使用自定义编码器
json_str = json.dumps(data, cls=MyEncoder, ensure_ascii=False)
print(json_str)
# {"user": "admin", "login_time": "2026-08-01 08:30:00"}
```

```python
# 快速处理：使用 default 参数
json.dumps(data, default=str, ensure_ascii=False)
```

---

## 第二部分：CSV 模块

### 2.1 什么是 CSV？

**CSV**（Comma-Separated Values）是以纯文本存储表格数据的格式，一行一条记录，字段用逗号分隔。

```csv
姓名,年龄,城市,分数
张三,25,北京,92
李四,30,上海,85
王五,28,广州,78
```

**特点**：
- 纯文本，兼容所有平台
- Excel / Google Sheets 可直接打开
- 适合数据分析、数据导入导出
- 只支持**二维表格**，不支持层级嵌套

### 2.2 核心对象

| 类 | 方向 | 返回格式 |
|----|------|---------|
| `csv.reader(f)` | 读取 | 每行是 **列表** |
| `csv.writer(f)` | 写入 | 写入列表 |
| `csv.DictReader(f)` | 读取 | 每行是 **字典**（首行为键） |
| `csv.DictWriter(f, fieldnames)` | 写入 | 写入字典 |

### 2.3 基础操作

#### 写入 CSV

```python
import csv

# 方式一：普通 writer（列表写入）
with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # 写表头
    writer.writerow(["姓名", "年龄", "城市", "分数"])

    # 写单行
    writer.writerow(["张三", 25, "北京", 92])

    # 写多行
    rows = [
        ["李四", 30, "上海", 85],
        ["王五", 28, "广州", 78],
        ["赵六", 22, "深圳", 95],
    ]
    writer.writerows(rows)

print("students.csv 写入完成")
```

```python
# 方式二：DictWriter（字典写入）
with open("students2.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["姓名", "年龄", "城市", "分数"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 必须先写表头
    writer.writeheader()

    writer.writerow({"姓名": "张三", "年龄": 25, "城市": "北京", "分数": 92})
    writer.writerows([
        {"姓名": "李四", "年龄": 30, "城市": "上海", "分数": 85},
        {"姓名": "王五", "年龄": 28, "城市": "广州", "分数": 78},
    ])
```

> ⚠️ **必须加 `newline=""`**：Windows 下不加会导致写入时行间出现多余空行。

#### 读取 CSV

```python
import csv

# 方式一：普通 reader（列表读取）
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 输出：
# ['姓名', '年龄', '城市', '分数']
# ['张三', '25', '北京', '92']
# ['李四', '30', '上海', '85']
```

```python
# 方式二：DictReader（字典读取，推荐！）
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['姓名']} | {row['年龄']}岁 | {row['城市']} | {row['分数']}分")

# 输出：
# 张三 | 25岁 | 北京 | 92分
# 李四 | 30岁 | 上海 | 85分
```

### 2.4 实战：CSV 数据查询与分析

```python
import csv

def query_students(csv_path, min_score=0, city=None):
    """查询 CSV 中满足条件的学生"""
    results = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            score = int(row["分数"])
            if score >= min_score and (city is None or row["城市"] == city):
                results.append(row)

    return results

# 使用示例
high_scorers = query_students("students.csv", min_score=85)
beijing_students = query_students("students.csv", city="北京")
print(high_scorers)
```

### 2.5 高级参数

```python
# 自定义分隔符（如 TSV：Tab 分隔）
writer = csv.writer(f, delimiter="\t")

# 自定义引号处理
writer = csv.writer(f, quoting=csv.QUOTE_ALL)      # 所有字段加引号
writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC) # 非数字字段加引号

# 处理特殊换行符
reader = csv.reader(f, lineterminator="\n")
```

---

## 第三部分：pathlib 模块

### 3.1 什么是 pathlib？

`pathlib` 是 Python 3.4+ 引入的**面向对象路径操作库**，是 `os.path` 的现代化替代方案。一切皆 `Path` 对象，而不是字符串。

**核心理念**：
- 旧方式：`os.path.join(base, subdir, filename)`  — 字符串思维
- 新方式：`base / subdir / filename` — 路径对象思维，更直观

### 3.2 创建路径对象

```python
from pathlib import Path

# 当前工作目录
cwd = Path.cwd()
print(cwd)   # e:\Codework

# 用户主目录
home = Path.home()

# 直接创建
p = Path("e:/Codework/data.txt")

# 用 / 拼接路径（推荐！）
base = Path("e:/Codework")
json_file = base / "data" / "students.json"
print(json_file)   # e:\Codework\data\students.json

# 字符串与 Path 混合拼接
download_dir = Path.home() / "Downloads"
project_dir = Path.cwd() / "project"
```

> 💡 **技巧**：使用正斜杠 `/` 拼接，`pathlib` 会自动适配操作系统路径分隔符。

### 3.3 路径信息获取

```python
from pathlib import Path

p = Path("e:/Codework/project/data/report.xlsx")

print(p.name)       # report.xlsx      文件名（含扩展名）
print(p.stem)       # report           文件名（不含扩展名）
print(p.suffix)     # .xlsx            扩展名
print(p.suffixes)   # ['.xlsx']        多级扩展名
print(p.parent)     # e:\Codework\project\data   父目录
print(p.parent.parent)  # e:\Codework\project     祖父目录
print(p.parts)      # ('e:\\', 'Codework', 'project', 'data', 'report.xlsx')

# 修改后缀
new_p = p.with_suffix(".csv")
print(new_p)        # e:\Codework\project\data\report.csv

# 修改文件名
new_p = p.with_stem("summary")
print(new_p)        # e:\Codework\project\data\summary.xlsx
```

### 3.4 目录操作

#### 创建与遍历目录

```python
from pathlib import Path

# 创建单层目录，存在也不报错
Path("output").mkdir(exist_ok=True)

# 创建多层目录
(Path("output") / "images" / "thumbnails").mkdir(parents=True, exist_ok=True)
# parents=True  → 类似 mkdir -p，自动创建父目录
# exist_ok=True → 目录存在不报错

# 遍历目录（只列当前层）
base = Path("e:/Codework")
for item in base.iterdir():
    if item.is_file():
        print(f"[文件] {item.name}")
    elif item.is_dir():
        print(f"[目录] {item.name}")

# 输出：
# [文件] exp3.py
# [文件] exp4.py
# [目录] project
# [目录] python在线笔记
# ...
```

#### glob 模式匹配（非常重要！）

```python
from pathlib import Path

base = Path("e:/Codework")

# 匹配所有 .py 文件（当前层）
for py_file in base.glob("*.py"):
    print(py_file.name)

# 递归匹配所有 .md 文件（包括子目录）
for md_file in base.rglob("*.md"):
    rel_path = md_file.relative_to(base)
    print(rel_path)

# 复杂匹配
base.rglob("test*.txt")      # 以 test 开头的 .txt
base.glob("exp[0-9].py")    # exp0.py 到 exp9.py
base.rglob("**/data/*.json")  # 任意 data 子目录下的 json 文件
```

**`glob` vs `rglob`**：
- `glob(pattern)`：只在当前目录匹配
- `rglob(pattern)`：递归匹配所有子目录（等价于 `glob("**/" + pattern)`）

### 3.5 文件读写（极简方式！）

```python
from pathlib import Path

p = Path("data.txt")

# 读取全部文本
content = p.read_text(encoding="utf-8")

# 按行读取
lines = p.read_text(encoding="utf-8").splitlines()

# 写入文本
p.write_text("Hello, pathlib!", encoding="utf-8")

# 追加写入
old = p.read_text(encoding="utf-8")
p.write_text(old + "\nNew line", encoding="utf-8")

# 读取二进制
bytes_data = Path("image.png").read_bytes()

# 写入二进制
Path("output.bin").write_bytes(bytes_data)
```

> 告别 `with open(...) as f: f.read()` — pathlib 一行搞定！

### 3.6 文件与目录判断

```python
from pathlib import Path

p = Path("test.txt")

p.exists()       # 路径是否存在
p.is_file()      # 是否为文件
p.is_dir()       # 是否为目录
p.is_symlink()   # 是否为符号链接
p.is_absolute()  # 是否为绝对路径

# 获取文件信息
stat = p.stat()
print(f"大小: {stat.st_size} bytes")          # 文件大小
print(f"修改时间: {stat.st_mtime}")            # 最后修改时间戳
```

### 3.7 文件与目录管理

```python
from pathlib import Path

p = Path("old_name.txt")

# 重命名（可同时移动）
p.rename("new_name.txt")
p.rename(Path("backup") / "archived.txt")

# 删除文件（目录非空无法删除）
p.unlink(missing_ok=True)
# missing_ok=True → Py3.8+，文件不存在也不报错

# 创建空文件
Path("new_file.txt").touch()

# 删除空目录
Path("empty_dir").rmdir()
```

### 3.8 综合应用：目录扫描器

```python
from pathlib import Path

def scan_directory(directory_path):
    """扫描目录，按扩展名分类统计"""
    stats = {}

    for file in Path(directory_path).iterdir():
        if file.is_file():
            ext = file.suffix.lower() or "(无扩展名)"
            stats.setdefault(ext, []).append(file.name)

    # 打印统计
    print(f"目录: {directory_path}")
    print("-" * 40)
    for ext, files in sorted(stats.items()):
        print(f"{ext:.<15} {len(files):>3} 个文件")
        for f in files[:3]:  # 每种只印前 3 个
            print(f"  └─ {f}")
        if len(files) > 3:
            print(f"  └─ ... 还有 {len(files) - 3} 个")

# 使用
scan_directory("e:/Codework")
```

---

## 第四部分：三种工具的对比与选择

| 特性 | JSON | CSV | pathlib |
|------|------|-----|---------|
| **用途** | 数据交换与存储 | 表格数据存储 | 文件系统操作 |
| **数据结构** | 层级嵌套（对象、数组） | 二维表格 | 不是数据格式 |
| **可读性** | 人类与机器均可读 | 人类可读，Excel 打开 | N/A |
| **写入方式** | `json.dump(data, f)` | `csv.writer(f)` | `Path.write_text(data)` |
| **读取方式** | `json.load(f)` | `csv.reader(f)` | `Path.read_text()` |
| **中文支持** | `ensure_ascii=False` | `encoding="utf-8"` | `encoding="utf-8"` |
| **跨语言** | 所有主流语言支持 | 通用标准 | Python 专属 |

### 选择决策

```
需要存哪类数据？
├─ 配置、嵌套结构、API 返回  → JSON
├─ 表格数据、Excel 导出      → CSV
├─ 只需操作文件/目录          → pathlib
└─ 三者配合（常见场景）      → pathlib 管路径 + JSON/CSV 管内容
```

---

## 第五部分：综合实战演练

### 练习一：通讯录 JSON 持久化

将你现有的通讯录数据保存为 JSON，实现启动加载 + 退出保存。

```python
import json
from pathlib import Path

class ContactBook:
    """JSON 持久化的通讯录"""
    def __init__(self, filepath="contacts.json"):
        self.filepath = Path(filepath)
        self.contacts = []
        self.load()

    def load(self):
        """从文件加载通讯录"""
        if self.filepath.exists():
            try:
                data = json.loads(self.filepath.read_text(encoding="utf-8"))
                self.contacts = data
                print(f"📖 已加载 {len(self.contacts)} 条联系人")
            except (json.JSONDecodeError, KeyError):
                print("⚠️  文件损坏，使用空通讯录")
                self.contacts = []

    def save(self):
        """保存通讯录到文件"""
        self.filepath.write_text(
            json.dumps(self.contacts, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )
        print(f"💾 已保存 {len(self.contacts)} 条联系人")

    def add(self, name, phone, email=""):
        contact = {"name": name, "phone": phone, "email": email}
        self.contacts.append(contact)
        print(f"✅ 已添加: {name}")

    def list_all(self):
        if not self.contacts:
            print("通讯录为空")
            return
        for i, c in enumerate(self.contacts, 1):
            print(f"{i}. {c['name']} | {c['phone']} | {c['email']}")

    def search(self, keyword):
        results = [
            c for c in self.contacts
            if keyword in c["name"] or keyword in c["phone"]
        ]
        if results:
            for c in results:
                print(f"🔍 {c['name']} | {c['phone']} | {c['email']}")
        else:
            print(f"未找到包含 '{keyword}' 的联系人")


# 使用示例
if __name__ == "__main__":
    book = ContactBook("my_contacts.json")
    book.add("张三", "13800138000", "zhangsan@email.com")
    book.add("李四", "13900139000")
    book.list_all()
    book.search("张")
    book.save()  # 程序退出时保存
```

### 练习二：CSV 转为 JSON

```python
import csv
import json
from pathlib import Path

def csv_to_json(csv_path, json_path):
    """将 CSV 文件转为 JSON 文件"""
    records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    Path(json_path).write_text(
        json.dumps(records, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )
    print(f"✅ 转换完成: {csv_path} → {json_path} ({len(records)} 条)")

# 使用
csv_to_json("students.csv", "students.json")
```

### 练习三：文件自动分类器 CLI

这是你学习计划中的核心实战任务！扫描目录 → 按扩展名分类移动文件。

```python
import shutil
from pathlib import Path
from collections import defaultdict


def classify_files(source_dir, dry_run=True):
    """
    按扩展名将文件分类到子目录

    参数:
        source_dir: 要整理的目录路径
        dry_run: True 则只预览不实际移动
    """
    source = Path(source_dir)
    if not source.is_dir():
        print(f"❌ 目录不存在: {source_dir}")
        return

    # 扫描文件并分类
    file_groups = defaultdict(list)
    for f in source.iterdir():
        if f.is_file():
            ext = f.suffix.lower().lstrip(".")
            if ext == "":
                ext = "no_extension"
            file_groups[ext].append(f)

    if not file_groups:
        print("没有文件需要分类")
        return

    # 移动文件
    total = 0
    for ext, files in sorted(file_groups.items()):
        target_dir = source / ext
        print(f"\n📁 [{ext}] {len(files)} 个文件")

        # 创建目标目录
        if not dry_run:
            target_dir.mkdir(exist_ok=True)

        for f in files:
            print(f"   {'[预览]' if dry_run else '→'} {f.name}")
            if not dry_run:
                shutil.move(str(f), str(target_dir / f.name))
        total += len(files)

    if dry_run:
        print(f"\n⚠️  [预览模式] 共 {total} 个文件，实际未被移动。请添加 --no-dry-run 参数执行。")
    else:
        print(f"\n✅ 分类完成！共 {total} 个文件 → {source_dir}")


if __name__ == "__main__":
    import sys

    # 简单参数解析（学习计划后续会用 argparse 升级）
    dry_run = "--no-dry-run" not in sys.argv
    source = sys.argv[1] if len(sys.argv) > 1 else "."

    print(f"📂 源目录: {source}")
    classify_files(source, dry_run=dry_run)
```

### 练习四：三剑客联动 — 项目配置文件管理

```python
import json
import csv
from pathlib import Path


class ProjectManager:
    """项目管理器：JSON 存配置，CSV 存数据，pathlib 管路径"""

    def __init__(self, project_root):
        self.root = Path(project_root)
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def config_path(self):
        return self.root / "config.json"

    @property
    def data_path(self):
        return self.root / "data.csv"

    def init_project(self, config: dict):
        """初始化项目配置（JSON）"""
        self.config_path.write_text(
            json.dumps(config, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )
        print(f"✅ 配置已写入: {self.config_path}")

    def save_records(self, records: list[dict], fieldnames: list[str]):
        """保存数据记录（CSV）"""
        with open(self.data_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        print(f"✅ {len(records)} 条数据已写入: {self.data_path}")

    def list_files(self):
        """列出项目下所有文件"""
        print(f"📂 项目: {self.root}")
        for f in sorted(self.root.rglob("*")):
            if f.is_file():
                size = f.stat().st_size
                print(f"  {f.relative_to(self.root)} ({size} bytes)")


# 使用
pm = ProjectManager("./my_project")
pm.init_project({"app_name": "MyApp", "version": "1.0", "debug": False})

pm.save_records(
    [{"id": "1", "title": "学习JSON", "status": "done"},
     {"id": "2", "title": "学习CSV",  "status": "doing"},
     {"id": "3", "title": "学习pathlib", "status": "todo"}],
    fieldnames=["id", "title", "status"]
)

pm.list_files()
```

---

## 第六部分：自测练习

### 基础题（必做）

1. **JSON 读写**：创建一个包含个人信息的字典（姓名、年龄、技能列表），用 `json.dump` 保存，再用 `json.load` 读出并打印。

2. **CSV 读写**：创建 3 条商品记录（商品名、价格、库存），用 `csv.DictWriter` 写入文件，再用 `csv.DictReader` 读出并计算总库存。

3. **pathlib 遍历**：用 `rglob` 找出当前项目目录下所有 `.py` 文件，打印文件名和大小。

### 进阶题

4. **JSON → CSV 转换器**：读取一个 JSON 文件（假设内容是对象数组），将其转换为同一目录下同名的 CSV 文件。

5. **CSV 数据过滤**：读取学生成绩 CSV，筛选分数 ≥ 80 的学生，写入新的 CSV `pass_students.csv`。

### 综合题（周考级别）

6. **文件自动分类器**：不看答案完整实现上面的文件分类器，要求：
   - 用 `pathlib` 扫描目录
   - 用 `rglob` 统计子目录文件情况
   - 按扩展名分类到对应文件夹
   - 支持 `--dry-run` 预览模式
   - （加分）用 `json` 保存操作日志（记录时间、移动的文件名、来源与目标路径）

---

## 附录：速查卡片

### JSON 速查

```python
import json

# 保存
json.dump(obj, file, ensure_ascii=False, indent=4)

# 读取
data = json.load(file)

# 字符串互转
s = json.dumps(obj, ensure_ascii=False)
obj = json.loads(s)
```

### CSV 速查

```python
import csv

# 写入
writer = csv.DictWriter(f, fieldnames=fields)
writer.writeheader()
writer.writerows(rows)

# 读取（推荐 DictReader）
reader = csv.DictReader(f)
for row in reader:
    print(row["列名"])
```

### pathlib 速查

```python
from pathlib import Path

Path("dir").mkdir(parents=True, exist_ok=True)
list(Path(".").glob("*.py"))        # 当前层匹配
list(Path(".").rglob("**/*.py"))    # 递归匹配
text = Path("file.txt").read_text(encoding="utf-8")
Path("out.txt").write_text("hi", encoding="utf-8")
Path("old").rename("new")
Path("file").unlink(missing_ok=True)
```

---

> 📌 **下一步**：Day 5 下午的任务是用这三个工具完成「文件自动分类器 CLI」和「JSON 版通讯录」。祝你学习顺利！
