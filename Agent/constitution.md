# Stock Report Hunt - Agent Constitution
Last Updated: 2025-01-27

## 继承规范
本项目遵循 `/cc/.claude` (CLAUDE.md) 中的核心规范。

## 项目特定规则

### 1. 数据源优先级
1. SEC EDGAR (官方财报)
2. 公司 Investor Relations 页面 (Earnings Call)
3. 第三方数据源 (如需要)

### 2. 输出格式
- 财报：Markdown (.md)
- 音频/视频：保持原格式
- 所有文件存入 `downloads/<TICKER>/`

### 3. 安全规则
- User-Agent 通过环境变量 `SEC_USER_AGENT` 配置
- 不存储任何用户凭证

### 4. 依赖原则
- 优先使用纯 Python 库，避免系统级依赖
- 新依赖需记录在 ADR 中
