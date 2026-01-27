# 日历 + Watchlist 测试指南
Last Updated: 2026-01-27

## 准备工作

1. 确保依赖已安装:
   ```bash
   pip install -r requirements.txt
   ```

2. 启动 Web UI:
   ```bash
   streamlit run app.py
   ```

## 测试步骤

### 测试 1: Watchlist 管理

1. 在侧边栏输入框输入 `AAPL`
2. 点击「添加」按钮
3. 预期结果:
   - 侧边栏显示 AAPL
   - 项目目录生成 `watchlist.txt` 文件

4. 点击 AAPL 旁边的 ❌ 按钮
5. 预期结果:
   - AAPL 从列表中移除

### 测试 2: 日历视图

1. 添加 AAPL, NVDA, MSFT 到 Watchlist
2. 点击「财报日历」标签页
3. 预期结果:
   - 显示「正在获取财报日期...」
   - 加载完成后显示按月份分组的事件表格
   - 每个事件显示日期、股票代码、类型

### 测试 3: 批量下载

1. 确保 Watchlist 中有至少 2 只股票
2. 在日历页面底部勾选「SEC 财报」和「Earnings Call」
3. 点击「下载全部 Watchlist」
4. 预期结果:
   - 显示下载进度条
   - 完成后显示成功消息
   - `downloads/` 目录下有对应股票的文件夹

### 测试 4: 配置文件格式

1. 手动创建 `watchlist.txt`:
   ```
   # 我的关注列表
   AAPL, NVDA
   MSFT
   ```

2. 刷新页面
3. 预期结果:
   - 侧边栏显示 AAPL, NVDA, MSFT

## 常见问题

- **日历加载慢**: 需要逐个查询每只股票的日期，股票越多越慢
- **某些股票无日期**: 部分股票可能在 Motley Fool 上没有数据
