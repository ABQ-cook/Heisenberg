# open-source-learning（开源项目学习区）

本目录用于存放我挑选的、用来**精读 → 复现 → 延伸**的 GitHub 开源项目。
学习目标：补齐**生产级后端工程**手感 + **Agent 应用开发**能力，最终产出能写进简历、能经得起面试追问的作品。

## 目录内容

| 项目 | 定位 | 学习说明 |
|------|------|----------|
| `full-stack-fastapi-template/` | 后端地基（FastAPI 官方全栈模板） | [README-zh.md](full-stack-fastapi-template/README-zh.md) |
| `openai-agents-python/` | Agent 应用（OpenAI 官方 Agents SDK） | [README-zh.md](openai-agents-python/README-zh.md) |

> 两个子目录各自带有独立的 `.git`（克隆自 GitHub），它们是"嵌套仓库"，不要把它们 add 进外层 Codework 的 Git 仓库。

## 推荐学习节奏（总预算约 4 周，优先级从高到低）

1. **第 1-2 周**：`full-stack-fastapi-template` —— 跑通 → 精读后端分层 → 改造成自己的管理系统。
2. **第 3-4 周**：`openai-agents-python` —— 跑通官方示例 → 用 DeepSeek 复现"带工具的 Agent" → 用 FastAPI 封装成一个能演示的 Agent 应用。
3. **之后视时间追加**：行业级参考项目（Dify / Langchain-Chatchat 二选一），定位"读 + 提一个 PR"，不要贪多。

## 重要约定

- **复现 ≠ 抄代码**：学习时每看完一个模块，合上代码用自己的话重新实现一遍；卡住再回来看。
- **延伸是差异化**：每个仓库至少做 1 个"上游没有、你想加"的功能，并记录对比结论（数据/截图）。
- **提交前想清楚**：这两个目录最初来自别人的仓库，学习过程中写的代码如果推回自己的 GitHub，请先 **Fork 一份**再推到自己的 fork，不要直接 push 到上游（也没有权限）。
- 国内网络拉取 GitHub 偶发中断，可参考外层总 README 所在会话的说明：用 `git -c http.version=HTTP/1.1 clone` 或浅克隆重试。
