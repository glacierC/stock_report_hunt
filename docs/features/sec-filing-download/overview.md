# SEC 财报下载功能
Last Updated: 2025-01-27

## 这是什么
输入美股代码（如 AAPL），自动从 SEC EDGAR 下载最新的年报（10-K）和季报（10-Q）。

## 给谁用
需要快速获取美股公司官方财报的投资研究者。

## 怎么用
```bash
python main.py AAPL
```

## 会发生什么
1. 工具自动查询 SEC 数据库
2. 下载最新的 10-K 和 10-Q 文件
3. 转换成可读的 Markdown 格式
4. 自动打开下载文件夹
5. 显示你的分析 prompt（如果有 my_prompt.txt）

## 文件存放位置
```
downloads/
└── AAPL/
    ├── AAPL_10-K_2025-10-31.md
    └── AAPL_10-Q_2025-08-01.md
```
