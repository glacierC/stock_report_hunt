# Roadmap: Stock Hunter (美股财报自动抓取助手)
Last Updated: 2026-01-27

## 1. 项目一句话
这是一个“自动化美股资料收集器”。用户输入股票代码，工具自动查询下一次财报/电话会时间，并自动去 SEC 官网下载最新的财报文件到本地，同时调出用户预设好的 Prompt，辅助用户进行 Deep Research 分析。

## 2. Key Assumptions (关键假设)
- **Prompt 管理**：用户会自己在本地维护一个 `my_prompt.txt` 文件，工具**只读不写**（只负责打开或复制，不负责生成内容）。
- **分析方式**：完全依赖用户手动将文件拖入外部 ChatBot，本工具不集成 LLM API。
- **数据源**：v0.1 仅依赖 SEC (EDGAR) 官方源。

## 3. Version Planning

### v0.1 ✅ (已完成: 抓取与交付)
**Goal**: 极速获取“最新财报 PDF” + “我的分析咒语”。
- **Scope**:
  - [配置] 允许用户在根目录放置一个 `my_prompt.txt` (内存放用户自己的分析指令)。
  - [下载] 输入 Ticker (如 AAPL)，自动从 SEC 下载最新的 10-Q/10-K PDF 到 `downloads/AAPL/`。
  - [交付] 下载完成后，自动做两件事：
    1. **打开文件夹**（展示 PDF）。
    2. **自动读取并展示/复制** `my_prompt.txt` 的内容，或者直接打开这个文本文件。
- **Acceptance (点击验收)**:
  1. 我在项目根目录放好了一个 `my_prompt.txt`（写着：请分析这家公司的护城河...）。
  2. 运行工具，输入 `NVDA`。
  3. 几秒后，电脑自动弹出一个窗口，里面有 `NVDA_2024_10Q.pdf`。
  4. 同时，终端显示（或自动打开了）我的 `my_prompt.txt` 内容，方便我直接复制。
- **Dependencies**:
  - SEC EDGAR 访问库 (如 `sec-edgar-downloader`)。
  - 必须设置 User-Agent。

### v0.2 ✅ (已完成: Human Readable / 可读性清洗)
**Goal**: 把下载下来的“天书”变成人类和 AI 都能流畅阅读的格式。
- **Scope**:
  - [过滤] 自动识别 Submission 中的 "Primary Document" (主文档)，抛弃 XML/XBRL 等乱码文件。
  - [转换] 将提取出的 HTML 财报转换为 **PDF** (优先) 或 **Markdown** (纯文本)。
  - [瘦身] 去除冗余的 HTML 标签、样式表，只保留正文和数据表格。
- **Acceptance (点击验收)**:
  1. 运行工具，输入 `AAPL`。
  2. 文件夹自动打开。
  3. **关键点**：原本几十兆的 `.txt` 乱码文件不见了，取而代之的是一个干净的 `AAPL_2024_10K.pdf` (或 .md)。
  4. 我双击打开文件，看到的是整洁的段落和表格，没有代码。
- **Dependencies**:
  - `requests` + `beautifulsoup4` - 直接调用 SEC API
  - `markdownify` - HTML 转 Markdown (纯 Python，无系统依赖)

### v0.3 ✅ (已完成: Earnings Call 抓取)
**Goal**: 自动抓取公司 Earnings Call transcript。

- **Scope**:
  - [发现] 从 Motley Fool 公司页面查找 transcript 链接
  - [抓取] 下载完整 Earnings Call transcript (含 Takeaways, Summary)
  - [整合] 保存到 `downloads/<TICKER>/`

- **数据源**: The Motley Fool (免费爬取)
- **输出**: Markdown 格式 (~50KB)

- **Acceptance (点击验收)**:
  1. 运行 `python main.py AAPL --earnings`
  2. 文件夹自动打开
  3. 看到 `AAPL_earnings_YYYYMMDD.md`
  4. 内容包含完整 transcript、关键数据、CEO 引用

### v0.4 ✅ (已完成: Web UI + 整合查询)
**Goal**: 提供本地 Web 界面，支持公司名称模糊匹配，一键获取财报 + Earnings Call。

- **Scope**:
  - [Web UI] 使用 Streamlit 构建本地网页界面
    - 输入框支持股票代码（AAPL）或公司名称（Apple）
    - 公司名称模糊匹配 → 自动转换为 Ticker
    - 一键同时下载 SEC 财报 + Earnings Call transcript
    - 页面显示下载结果、文件链接、报告日期
  - [CLI 增强] 命令行输出最新报告发布时间
  - [灵活性] 保留现有参数（`--earnings`, `--no-sec`）

- **Dependencies**:
  - `streamlit` - Web UI 框架
  - 公司名称 → Ticker 映射（SEC 或第三方数据）

- **Acceptance (点击验收)**:
  1. 运行 `streamlit run app.py`
  2. 浏览器打开 `http://localhost:8501`
  3. 输入 "Apple"，系统自动识别为 AAPL
  4. 点击下载，页面显示：
     - SEC 10-K/10-Q 文件链接
     - Earnings Call transcript 链接
     - 各报告的发布日期
  5. CLI 仍可用：`python main.py AAPL` 输出包含报告时间

---

## 4. 已完成 (Done)

| Version | 完成日期 | 关键交付 |
|---------|----------|----------|
| v0.1 | 2025-01-26 | SEC 财报下载 + prompt 展示 |
| v0.2 | 2025-01-26 | HTML 转 Markdown，文件瘦身 |
| v0.3 | 2025-01-27 | Earnings Call transcript (Motley Fool) |
| v0.4 | 2026-01-27 | Streamlit Web UI + 模糊匹配 |

---

## 5. 未来规划

### v1.0 (未来: 日历 + Watchlist)
**Goal**: 可视化追踪关注股票的财报和 Earnings Call 日期。

- **Scope**:
  - [Watchlist] 配置文件 `watchlist.txt` 管理关注的股票列表
  - [日历视图] Web UI 显示：
    - Watchlist 中所有股票
    - 每只股票的财报发布日期
    - Earnings Call 日期
  - [数据源] 优先使用 Motley Fool，不行再换其他 API
  - [批量操作] 一键下载 Watchlist 中所有股票的最新资料

- **Acceptance (点击验收)**:
  1. 创建 `watchlist.txt`，写入 AAPL, NVDA, MSFT
  2. 打开 Web UI，看到日历视图
  3. 日历上标注各股票的财报日期和 Earnings Call 日期
  4. 点击某日期，可查看/下载对应股票的资料

