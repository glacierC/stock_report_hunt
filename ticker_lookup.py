#!/usr/bin/env python3
"""
公司名称 → Ticker 模糊匹配
数据源: SEC EDGAR company tickers
"""

import json
import os
import re
from pathlib import Path

import requests

HEADERS = {
    "User-Agent": os.environ.get("SEC_USER_AGENT", "MyApp contact@example.com"),
}

# 缓存文件路径
CACHE_FILE = Path(__file__).parent / ".ticker_cache.json"


def fetch_company_tickers() -> dict:
    """从 SEC 获取公司 ticker 列表"""
    url = "https://www.sec.gov/files/company_tickers.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def load_ticker_data() -> list[dict]:
    """加载 ticker 数据（优先使用缓存）"""
    # 检查缓存
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text())
            if data:  # 缓存有效
                return data
        except (json.JSONDecodeError, KeyError):
            pass

    # 从 SEC 获取
    raw_data = fetch_company_tickers()

    # 转换格式: {0: {cik_str, ticker, title}, ...} -> [{cik, ticker, name}, ...]
    companies = []
    for item in raw_data.values():
        companies.append({
            "cik": str(item["cik_str"]),
            "ticker": item["ticker"].upper(),
            "name": item["title"],
        })

    # 保存缓存
    CACHE_FILE.write_text(json.dumps(companies, ensure_ascii=False))

    return companies


def search_ticker(query: str, limit: int = 10) -> list[dict]:
    """
    模糊搜索公司

    Args:
        query: 股票代码或公司名称
        limit: 返回结果数量限制

    Returns:
        匹配的公司列表 [{ticker, name, cik}, ...]
    """
    query = query.strip().upper()
    if not query:
        return []

    companies = load_ticker_data()

    # 精确匹配 ticker
    for company in companies:
        if company["ticker"] == query:
            return [company]

    # 模糊匹配
    results = []
    query_lower = query.lower()

    for company in companies:
        ticker = company["ticker"]
        name = company["name"]
        name_lower = name.lower()

        # ticker 开头匹配
        if ticker.startswith(query):
            results.append((0, len(ticker), company))  # 优先级最高，短 ticker 优先
        # 公司名称精确开头匹配 (如 "Apple Inc." 匹配 "apple")
        elif name_lower.startswith(query_lower + " ") or name_lower == query_lower:
            results.append((1, len(name), company))
        # 公司名称开头匹配
        elif name_lower.startswith(query_lower):
            results.append((2, len(name), company))
        # 公司名称包含查询词
        elif query_lower in name_lower:
            results.append((3, len(name), company))

    # 按优先级排序，同优先级按名称长度排序（短的优先）
    results.sort(key=lambda x: (x[0], x[1]))

    return [r[2] for r in results[:limit]]


def get_ticker(query: str) -> str | None:
    """
    获取最匹配的 ticker

    Args:
        query: 股票代码或公司名称

    Returns:
        ticker 或 None
    """
    results = search_ticker(query, limit=1)
    if results:
        return results[0]["ticker"]
    return None


if __name__ == "__main__":
    # 测试
    import sys

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"搜索: {query}\n")
        results = search_ticker(query)
        for r in results:
            print(f"  {r['ticker']:6} - {r['name']}")
    else:
        print("用法: python ticker_lookup.py <公司名称或代码>")
