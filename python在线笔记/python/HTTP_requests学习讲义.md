# HTTP 与 requests 库学习讲义

> 对应学习计划：Week 1 Day 6 — 周二 7/28：HTTP + requests
>
> 学习目标：掌握 HTTP 请求/响应基本概念，熟练使用 requests 库发起 GET/POST 请求，搞清 `params` vs `data` vs `json` 三者的区别，完成 API 聚合器实战

---

## 目录

- [第一部分：HTTP 基础概念](#第一部分http-基础概念)
- [第二部分：requests 库入门](#第二部分requests-库入门)
- [第三部分：params vs data vs json 大对决](#第三部分params-vs-data-vs-json-大对决)
- [第四部分：异常处理与超时](#第四部分异常处理与超时)
- [第五部分：复用 Day 1 成果 —— @retry 装饰器](#第五部分复用-day-1-成果--retry-装饰器)
- [第六部分：综合实战 —— API 聚合器](#第六部分综合实战--api-聚合器)
- [第七部分：晚间八股](#第七部分晚间八股)
- [第八部分：自测练习](#第八部分自测练习)

---

## 第一部分：HTTP 基础概念

### 1.1 什么是 HTTP？

**HTTP**（HyperText Transfer Protocol，超文本传输协议）是 Web 世界最基础的**通信协议**，规定了客户端（浏览器、Python 程序）与服务器之间如何交换数据。

**核心模型：请求（Request）→ 响应（Response）**

```
┌──────────┐   发送请求    ┌──────────┐
│  客户端    │ ────────────▶ │  服务器   │
│ (你的程序) │ ◀──────────── │ (API 提供方)│
└──────────┘   返回响应    └──────────┘
```

> 你每次在浏览器输入网址，本质就是发出一个 HTTP 请求；网页加载出来，就是收到了服务器的 HTTP 响应。

### 1.2 HTTP 请求（Request）的结构

一个请求由 4 部分组成：

```
①请求行    POST /api/users HTTP/1.1
②请求头    Host: api.github.com
           Content-Type: application/json
           Authorization: Bearer xxx
③空行
④请求体    {"name": "张三", "age": 25}   ← 只有部分请求有
```

| 组成部分 | 作用 | 举例 |
|----------|------|------|
| 请求行 | 方法 + 路径 + 协议版本 | `GET /users HTTP/1.1` |
| 请求头（Headers） | 携带附加信息 | `Content-Type`、`Authorization` |
| 请求体（Body） | 携带要发送的数据 | 登录时的账号密码 |
| 空行 | 分隔头部和体部 | 协议格式要求 |

### 1.3 HTTP 响应（Response）的结构

服务器返回的响应也是 4 部分：

```
①状态行    HTTP/1.1 200 OK
②响应头    Content-Type: application/json
           Content-Length: 1024
③空行
④响应体    {"message": "success", "data": [...]}
```

| 组成部分 | 作用 | 举例 |
|----------|------|------|
| 状态行 | 状态码 + 原因短语 | `200 OK`、`404 Not Found` |
| 响应头 | 响应元信息 | `Content-Type` 告诉客户端返回什么格式 |
| 响应体 | 实际返回的数据 | JSON、HTML、图片等 |

### 1.4 常用 HTTP 方法

| 方法 | 含义 | 类比 | 有无请求体 |
|------|------|------|-----------|
| `GET` | 获取资源 | 查快递 | ❌ 无 |
| `POST` | 创建资源 | 下新订单 | ✅ 有 |
| `PUT` | 整体更新资源 | 重填整个表单 | ✅ 有 |
| `PATCH` | 部分更新资源 | 只改手机号 | ✅ 有 |
| `DELETE` | 删除资源 | 取消订单 | 通常无 |

> **核心认知**：GET 只读不写、POST 用于提交创建，这是理解 HTTP 的起点。

### 1.5 常见 HTTP 状态码（晚间八股第一项）

| 状态码 | 含义 | 场景 |
|--------|------|------|
| **2xx 成功** | | |
| `200 OK` | 请求成功 | 查询数据成功 |
| `201 Created` | 资源创建成功 | POST 创建用户成功 |
| `204 No Content` | 成功但无返回体 | DELETE 删除成功 |
| **3xx 重定向** | | |
| `301 Moved Permanently` | 永久重定向 | 域名换了，浏览器自动跳转 |
| `302 Found` | 临时重定向 | 未登录跳转到登录页 |
| **4xx 客户端错误** | | |
| `400 Bad Request` | 请求格式错误 | 参数不合法 |
| `401 Unauthorized` | 未认证 | 没带 token |
| `403 Forbidden` | 无权限 | 已登录但没资格访问 |
| `404 Not Found` | 资源不存在 | 网址打错了 |
| `429 Too Many Requests` | 请求过于频繁 | 被限流了 |
| **5xx 服务器错误** | | |
| `500 Internal Server Error` | 服务器内部错误 | 后端代码崩了 |
| `502 Bad Gateway` | 网关错误 | 上游服务挂了 |
| `503 Service Unavailable` | 服务不可用 | 服务器过载维护中 |

**记忆口诀**：
```
2xx 成功，3xx 跳转，4xx 是你错了，5xx 是它错了
```

---

## 第二部分：requests 库入门

### 2.1 安装与导入

```bash
pip install requests
```

```python
import requests
```

### 2.2 第一个 GET 请求

用 `httpbin.org` 这个测试网站练习——它专门用来回显你的请求，方便调试：

```python
import requests

resp = requests.get('https://httpbin.org/get')
print(resp.status_code)   # 200
print(resp.text)          # 原始文本（JSON 字符串）
print(resp.json())        # 解析为 dict
```

**`Response` 对象的常用属性和方法**：

| 成员 | 类型 | 说明 |
|------|------|------|
| `resp.status_code` | `int` | 状态码 |
| `resp.reason` | `str` | 原因短语（如 'OK'） |
| `resp.headers` | `dict` | 响应头 |
| `resp.text` | `str` | 响应体文本 |
| `resp.content` | `bytes` | 响应体字节（下载文件用） |
| `resp.json()` | `dict` | 把 JSON 响应体解析为字典 |
| `resp.ok` | `bool` | 状态码 < 400 则为 True |
| `resp.url` | `str` | 最终请求的完整 URL |

### 2.3 带参数的 GET：`params`

```python
import requests

# 传统方式：手动拼 URL
url = 'https://httpbin.org/get?page=1&size=10'

# requests 推荐方式：用 params 字典
params = {'page': 1, 'size': 10}
resp = requests.get('https://httpbin.org/get', params=params)

print(resp.url)
# https://httpbin.org/get?page=1&size=10
```

**`params` 的好处**：requests 会自动帮你 URL 编码（中文、特殊字符会被转义），还能接收列表值（重复参数）。

```python
params = {'tags': ['python', 'web']}
# 自动变成 ?tags=python&tags=web
```

### 2.4 POST 请求

```python
import requests

resp = requests.post('https://httpbin.org/post', json={'name': '张三', 'age': 25})
print(resp.status_code)   # 200
print(resp.json()['json'])  # {'name': '张三', 'age': 25}，服务器回显了发过去的数据
```

### 2.5 响应头与自定义请求头

```python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)',
    'Accept': 'application/json',
}
resp = requests.get('https://httpbin.org/headers', headers=headers)

# 读取响应头
print(resp.headers['Content-Type'])   # application/json
```

---

## 第三部分：params vs data vs json 大对决

> 这是 Day 6 上午的重点，面试也常问。三者决定了**数据以什么方式发送**。

### 3.1 概念对比

| 参数 | 用途 | 数据去向 | 适用方法 |
|------|------|----------|----------|
| `params` | 查询字符串参数 | **URL 的 ?后面** | GET 为主 |
| `data` | 表单格式数据 | **请求体**，`application/x-www-form-urlencoded` | POST/PUT |
| `json` | JSON 格式数据 | **请求体**，`application/json` | POST/PUT |

### 3.2 实际效果对比

```python
import requests

url = 'https://httpbin.org/anything'

# ① params → 进 URL 查询串
r1 = requests.post(url, params={'a': '1'})
print(r1.url)              # .../anything?a=1
print(r1.json()['args'])   # {'a': '1'}  → args 字段（查询参数）

# ② data → 表单编码进请求体
r2 = requests.post(url, data={'name': '张三'})
print(r2.json()['form'])   # {'name': '张三'} → form 字段（表单数据）
print(r2.json()['data'])   # 空，data 没编码时不显示

# ③ json → JSON 编码进请求体
r3 = requests.post(url, json={'name': '张三'})
print(r3.json()['json'])   # {'name': '张三'} → json 字段
```

### 3.3 关键区别速记

```python
# GET 只带 params（查询参数在 URL 里）
requests.get('https://api.com/users', params={'page': 2})

# POST 传 JSON 数据给后端
requests.post('https://api.com/users', json={'name': '张三'})

# POST 模拟 HTML 表单提交
requests.post('https://api.com/login', data={'username': 'a', 'password': 'b'})
```

| 使用场景 | 选哪个 |
|----------|--------|
| 查询/筛选条件 | `params` |
| 后端接口要求 JSON 格式（FastAPI 接口基本都是） | `json` |
| 模拟网页表单提交（`application/x-www-form-urlencoded`） | `data` |
| 上传文件 | `files`（进阶） |

> ⚠️ **易错点**：`json` 和 `data` 不能同时传同一份数据；`json={'a':1}` 传的是字典，requests 内部自动 `json.dumps` + 设置 `Content-Type: application/json`。

---

## 第四部分：异常处理与超时

### 4.1 为什么要处理异常？

网络请求的失败方式五花八门：没网、对方服务器挂了、超时、代理问题……**不处理的话程序直接崩溃**。

### 4.2 必须写的参数：`timeout`

```python
# ❌ 危险写法：不设超时，可能永远卡住
resp = requests.get('https://api.example.com')

# ✅ 正确写法：5 秒没响应就放弃
resp = requests.get('https://api.example.com', timeout=5)

# 更细粒度：连接超时 3 秒 + 读取超时 5 秒
resp = requests.get('https://api.example.com', timeout=(3, 5))
```

> **面试点**：`timeout` 不写 = 无限等待，生产环境必须写。

### 4.3 常见异常类型

| 异常 | 触发场景 |
|------|----------|
| `requests.ConnectionError` | 网络不通、DNS 解析失败 |
| `requests.Timeout` | 超过 timeout 没响应 |
| `requests.HTTPError` | 状态码 4xx/5xx（需配合 `raise_for_status()`） |
| `requests.RequestException` | 所有 requests 异常的**基类**（兜底捕获用它） |

### 4.4 异常处理的标准姿势

```python
import requests

def fetch_data(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()      # 状态码 4xx/5xx 时抛 HTTPError
        return resp.json()
    except requests.Timeout:
        print(f'请求超时: {url}')
        return {}
    except requests.ConnectionError:
        print(f'连接失败: {url}')
        return {}
    except requests.HTTPError as e:
        print(f'HTTP 错误: {e}')
        return {}
    except requests.RequestException as e:
        print(f'其他请求错误: {type(e).__name__}: {e}')
        return {}
```

**`raise_for_status()`**：状态码 2xx 时什么都不做；4xx/5xx 时抛异常。这样"状态码不对"也会进入异常处理流程，避免拿着错误数据继续跑。

> 💡 **异常继承链**：`RequestException` ← `ConnectionError`/`Timeout`/`HTTPError`。兜底捕获写 `RequestException` 即可，具体类型放前面精确处理。

---

## 第五部分：复用 Day 1 成果 —— @retry 装饰器

> Day 6 的关键设计：**今天要用的 `@retry` 装饰器，是 Day 1 手写过两遍的成果**。这就是工程化学习的意义——积累的代码随时复用。

### 5.1 复习 @retry 装饰器

Day 1 的成品（如果当时写的版本功能不全，今天顺手补强）：

```python
import time
from functools import wraps

def retry(max_tries: int = 3, delay: float = 1.0):
    '''失败重试装饰器：函数抛异常时，最多重试 max_tries 次'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_tries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_tries:
                        print(f'已重试 {max_tries} 次仍失败，放弃')
                        raise
                    print(f'第 {attempt} 次失败（{e}），{delay} 秒后重试...')
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
```

### 5.2 测试 @retry

```python
# 模拟一个不稳定接口：前 2 次抛异常，第 3 次成功
count = 0

@retry(max_tries=3, delay=1)
def unstable_api():
    global count
    count += 1
    if count < 3:
        raise requests.ConnectionError('模拟断网')
    return {'data': '成功'}

result = unstable_api()
print(result)   # 第 1 次失败... 第 2 次失败... 最终返回 {'data': '成功'}
```

### 5.3 组合使用：@retry 处理网络请求

```python
@retry(max_tries=3, delay=2)
def get_weather(city: str) -> dict:
    resp = requests.get(
        f'https://httpbin.org/get?city={city}',
        timeout=5
    )
    resp.raise_for_status()
    return resp.json()
```

网络不稳定时自动重试 3 次，每次都等 2 秒——**这个组合是 Day 6 下午实战的核心骨架**。

---

## 第六部分：综合实战 —— API 聚合器

> 对应 Day 6 下午：调 2-3 个真实 API，合并结果输出。

### 6.1 需求分析

做一个**天气信息聚合器**，功能：

1. 输入城市名
2. 同时请求 2 个 API（此处用 httpbin 模拟 + 可替换为真实天气 API）
3. 合并结果统一输出
4. 网络异常自动重试，全部失败有兜底提示

### 6.2 完整代码

```python
import requests
import time
from functools import wraps


def retry(max_tries: int = 3, delay: float = 1.0):
    '''失败重试装饰器'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_tries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_tries:
                        raise
                    print(f'  ⚠️ 第 {attempt} 次失败（{e}），{delay} 秒后重试...')
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


@retry(max_tries=3, delay=1)
def fetch_source(name: str, url: str, params: dict) -> dict:
    '''请求单个数据源（带超时 + 自动重试）'''
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    return resp.json()


def aggregate(city: str) -> dict:
    '''聚合多个数据源的结果'''
    sources = {
        '来源A(模拟)': 'https://httpbin.org/get',
        '来源B(模拟)': 'https://httpbin.org/get',
    }
    results = {}
    for name, url in sources.items():
        try:
            data = fetch_source(name, url, {'city': city})
            results[name] = data['args']      # httpbin 回显的参数
            print(f'  ✅ {name} 请求成功')
        except Exception as e:
            results[name] = f'获取失败: {e}'
            print(f'  ❌ {name} 请求失败: {e}')
    return results


def main() -> None:
    city = input('请输入城市名：').strip()
    print(f'\n正在查询 {city} 的天气信息...')
    data = aggregate(city)
    print('\n===== 聚合结果 =====')
    for source, info in data.items():
        print(f'{source}: {info}')


if __name__ == '__main__':
    main()
```

### 6.3 替换为真实 API 的模板

真正对接天气 API 时，只需改 `sources` 字典和解析逻辑：

```python
# 以和风天气为例（需先在 qweather.com 免费申请 key）
HEFENG_KEY = '你的key'

@retry(max_tries=3, delay=1)
def fetch_hefeng(city_id: str) -> dict:
    resp = requests.get(
        'https://devapi.qweather.com/v7/weather/now',
        params={'location': city_id, 'key': HEFENG_KEY},
        timeout=5
    )
    resp.raise_for_status()
    return resp.json()['now']    # {'temp': '28', 'text': '晴', ...}

# GitHub API 例子（无需 key，公开接口）
@retry(max_tries=3, delay=1)
def fetch_github_user(username: str) -> dict:
    resp = requests.get(f'https://api.github.com/users/{username}', timeout=5)
    resp.raise_for_status()
    data = resp.json()
    return {'name': data.get('name'), 'repos': data.get('public_repos')}
```

> ⚠️ **注意**：免费 API 一般有限流（如每小时 N 次），报 `429` 时稍等再试——这也是为什么需要 `@retry` + 合理延时。

### 6.4 聚合器的工程化要点

| 设计 | 原因 |
|------|------|
| 每个数据源一个函数 + `@retry` | 单点失败不影响整体 |
| `timeout=5` | 防止卡死 |
| `raise_for_status()` | 4xx/5xx 也能被发现 |
| 聚合层 try/except 兜底 | 单个源挂了也有占位结果 |
| 主函数只做输入输出 | 结构清晰，方便扩展 |

---

## 第七部分：晚间八股

### 7.1 常见 HTTP 状态码（背 5 条）

1. **`200 OK`**：请求成功，返回正常数据
2. **`301 Moved Permanently`**：永久重定向，浏览器自动跳转到新地址
3. **`401 Unauthorized`**：未认证，需要登录/token
4. **`403 Forbidden`**：已认证但无权限访问
5. **`404 Not Found`**：资源不存在
6. **`500 Internal Server Error`**：服务器内部错误

### 7.2 GET vs POST 区别（面试必问）

| 维度 | GET | POST |
|------|-----|------|
| 用途 | 获取资源（只读） | 提交数据/创建资源（写） |
| 数据位置 | URL 查询参数（`?`后面） | 请求体（Body） |
| 数据可见性 | 明文在 URL，可见 | 在请求体，相对隐蔽 |
| 浏览器回退 | 安全，无副作用 | 会重新提交表单 |
| 缓存 | 可被浏览器缓存 | 默认不缓存 |
| 数据长度 | 受 URL 长度限制 | 理论上无限制 |
| 安全性 | 低（参数暴露） | 相对高（但 HTTPS 才真正加密） |

**一句话面试回答**：GET 是只读的查询操作，参数拼在 URL 上、可缓存；POST 是提交数据创建资源，数据放请求体、不可缓存。**语义不同是根本，安全性只是附带区别**（实际都要靠 HTTPS）。

### 7.3 补充概念：幂等性（加分项）

- **GET/PUT/DELETE**：幂等——同样的请求执行 1 次和 100 次，服务器状态相同
- **POST**：非幂等——重复提交会创建多条记录

> 这也是为什么"刷新页面导致重复下单"要用 POST 的替代方案（如表单 token）来防重复。

---

## 第八部分：自测练习

### 练习 1：基础填空（上午学完做）

1. HTTP 请求由____、____、____、____ 四部分组成
2. 状态码 `404` 属于____类错误，`500` 属于____类错误
3. `params` 把数据放在____，`json` 把数据放在____
4. GET 请求的数据放在____，POST 的数据通常放在____

<details>
<summary>点击查看答案</summary>

1. 请求行、请求头、空行、请求体
2. 4xx 客户端错误 / 5xx 服务器错误
3. URL 查询串 / 请求体
4. URL / 请求体

</details>

### 练习 2：写代码（上午学完做）

用 httpbin.org 完成以下操作：

```python
import requests

# ① GET 请求 httpbin.org/get，params 传 {'name': '你名字', 'page': 1}
#    打印返回的 args
# ② POST 请求 httpbin.org/post，json 传 {'skill': 'python'}
#    打印返回的 json 字段
# ③ POST 请求 httpbin.org/post，data 传 {'form_key': 'form_value'}
#    打印返回的 form 字段
```

### 练习 3：异常处理（下午学完做）

写一个函数 `safe_get(url)`：

- 带 `timeout=5`
- 捕获 `Timeout`、`ConnectionError`、`HTTPError`
- 失败时返回 `None` 并打印原因
- 用不存在域名的 URL（如 `https://nonexistent-domain-xyz.com`）测试

### 练习 4：完整实战 —— GitHub 用户聚合器（下午产出）

写一个 CLI 程序 `github_aggregator.py`：

1. 输入 GitHub 用户名
2. 调用 `https://api.github.com/users/{username}` 获取基本信息（姓名、公开仓库数、粉丝数、创建时间）
3. 调用 `https://api.github.com/users/{username}/repos` 获取仓库列表
4. 合并输出：用户信息 + 按 star 数排序的前 3 个仓库
5. 要求：`@retry` 装饰器 + `timeout` + 异常处理 + 类型标注

**提示**：仓库数据在 `resp.json()` 返回的**列表**中，每个元素有 `name` 和 `stargazers_count` 字段。

### 练习 5：八股自测（晚间做）

- [ ] 说出 5 个 HTTP 状态码及其含义
- [ ] 说出 GET 和 POST 的 4 个区别
- [ ] 用自己的话说：什么是幂等，哪些方法幂等

---

## 知识点总结卡片

```
HTTP 请求 = 方法 + URL + 头 + 体（可选）
HTTP 响应 = 状态码 + 头 + 体
状态码   = 2xx成功 / 3xx重定向 / 4xx你错 / 5xx它错
GET      = 只读查询，数据放 URL (params)
POST     = 提交创建，数据放请求体 (json / data)
params   = URL 查询参数   → 自动编码，适合筛选条件
data     = 表单格式请求体 → application/x-www-form-urlencoded
json     = JSON 请求体    → application/json，FastAPI 接口首选
timeout  = 必须写！不写会无限等待
@retry   = Day 1 成果复用，网络请求的标配包装
raise_for_status() = 状态码不对就抛异常，别拿着坏数据继续跑
```

---

## 今日产出清单

- [ ] `httpbin` 练习脚本（params / data / json 三种用法）
- [ ] `safe_get` 异常处理函数
- [ ] `github_aggregator.py` API 聚合器（@retry + timeout + 异常处理）
- [ ] 推送 GitHub
- [ ] 八股笔记 5 条（状态码 + GET vs POST）
