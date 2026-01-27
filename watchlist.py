#!/usr/bin/env python3
"""
Watchlist 管理模块
"""

from pathlib import Path

WATCHLIST_FILE = Path(__file__).parent / "watchlist.txt"


def load_watchlist() -> list[str]:
    """加载 watchlist，返回 ticker 列表"""
    if not WATCHLIST_FILE.exists():
        return []

    tickers = []
    for line in WATCHLIST_FILE.read_text().strip().split("\n"):
        line = line.strip()
        # 跳过空行和注释
        if line and not line.startswith("#"):
            # 支持逗号分隔和单行格式
            for ticker in line.replace(",", " ").split():
                ticker = ticker.strip().upper()
                if ticker and ticker not in tickers:
                    tickers.append(ticker)
    return tickers


def save_watchlist(tickers: list[str]) -> None:
    """保存 watchlist"""
    content = "# Stock Watchlist\n# 每行一个股票代码，或用逗号分隔\n\n"
    content += "\n".join(t.upper() for t in tickers)
    WATCHLIST_FILE.write_text(content)


def add_to_watchlist(ticker: str) -> bool:
    """添加股票到 watchlist，返回是否成功"""
    ticker = ticker.strip().upper()
    if not ticker:
        return False

    tickers = load_watchlist()
    if ticker in tickers:
        return False

    tickers.append(ticker)
    save_watchlist(tickers)
    return True


def remove_from_watchlist(ticker: str) -> bool:
    """从 watchlist 移除股票，返回是否成功"""
    ticker = ticker.strip().upper()
    tickers = load_watchlist()

    if ticker not in tickers:
        return False

    tickers.remove(ticker)
    save_watchlist(tickers)
    return True


if __name__ == "__main__":
    # 测试
    print(f"Watchlist: {load_watchlist()}")
