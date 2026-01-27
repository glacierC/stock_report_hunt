# Story 001: 抓取财报并交付

## 用户故事
作为一个美股投资者，我想输入股票代码后自动下载最新财报 PDF，并自动打开文件夹，这样我可以快速拿去分析。

## 验收标准 (Acceptance Criteria)
1. 在项目根目录放好 `my_prompt.txt`
2. 运行 `python main.py NVDA`
3. 程序自动从 SEC 下载最新的 10-Q 或 10-K PDF 到 `downloads/NVDA/`
4. 下载完成后自动打开文件夹
5. 终端显示 `my_prompt.txt` 的内容，方便复制

## 技术要点
- 使用 `sec-edgar-downloader` 库
- 必须配置 User-Agent (SEC 要求)
- 错误处理要友好，不暴露堆栈
- 支持 macOS 打开文件夹 (`open` 命令)

## 非目标 (Out of Scope)
- 不集成 LLM API
- 不修改 `my_prompt.txt`
- 不下载 8-K 或其他表格
