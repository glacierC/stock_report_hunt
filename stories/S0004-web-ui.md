# S0004 - Web UI + 整合查询
Last Updated: 2026-01-27

## 状态: Done
## 完成时间: 2026-01-27

## 目标
提供 Streamlit 本地网页界面，支持公司名称模糊匹配，一键获取财报 + Earnings Call。

## 验收标准
- [x] 运行 `streamlit run app.py` 启动 Web 服务
- [x] 浏览器打开 `http://localhost:8501`
- [x] 输入 "Apple"，系统自动识别为 AAPL
- [x] 点击下载，页面显示：
  - SEC 10-K/10-Q 文件链接
  - Earnings Call transcript 链接
  - 各报告的发布日期
- [x] CLI 仍可用：`python main.py AAPL` 输出包含报告时间

## 涉及文件

### 代码
- `app.py` (新建) - Streamlit Web UI
- `ticker_lookup.py` (新建) - 公司名称 → Ticker 模糊匹配
- `main.py` (修改) - CLI 增加报告时间输出
- `requirements.txt` (修改) - 添加 streamlit

### 文档
- `docs/features/web-ui/overview.md`
- `docs/features/web-ui/test-guide.md`

## 技术方案
1. **模糊匹配**: 使用 SEC 的公司列表 API 获取 ticker 映射
2. **Web UI**: Streamlit 单页应用
   - 输入框 + 下载按钮
   - 结果区显示文件链接和日期
3. **复用现有逻辑**: 调用 main.py 中的下载函数

## 验收记录
- 2026-01-27: 代码实现完成
- ticker_lookup.py: 公司名称模糊匹配（SEC 数据源）
- app.py: Streamlit Web UI
- main.py: CLI 增加报告时间输出
