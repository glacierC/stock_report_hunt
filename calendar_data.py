#!/usr/bin/env python3
"""
日历数据模块 - 获取财报和 Earnings Call 日期（包含未来日期）
"""

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from main import get_cik, get_latest_filing, HEADERS


def get_sec_filing_dates(ticker: str) -> list[dict]:
    """
    获取 SEC 财报发布日期（历史）
    返回: [{"type": "10-K", "date": "2024-10-31", "ticker": "AAPL"}, ...]
    """
    results = []
    try:
        cik = get_cik(ticker)
        for form_type in ["10-K", "10-Q"]:
            filing = get_latest_filing(cik, form_type)
            if filing:
                results.append({
                    "ticker": ticker.upper(),
                    "type": form_type,
                    "date": filing["filing_date"],
                    "category": "SEC Filing",
                    "status": "past",
                })
    except Exception:
        pass
    return results


def get_next_earnings_date_yfinance(ticker: str) -> dict | None:
    """
    从 yfinance 获取下一个 Earnings 日期（含精确时间和盘前/盘后）
    """
    try:
        import yfinance as yf

        stock = yf.Ticker(ticker)
        info = stock.info

        earnings_ts = info.get("earningsTimestamp")
        if not earnings_ts:
            return None

        dt = datetime.fromtimestamp(earnings_ts)
        formatted_date = dt.strftime("%Y-%m-%d")
        formatted_time = dt.strftime("%H:%M") + " ET"

        # 判断盘前/盘后 (美股开盘 9:30, 收盘 16:00 EST)
        hour = dt.hour
        if hour < 9 or (hour == 9 and dt.minute < 30):
            timing = "BMO (盘前)"
        elif hour >= 16:
            timing = "AMC (盘后)"
        else:
            timing = "盘中"

        # 是否为预估日期
        is_estimate = info.get("isEarningsDateEstimate", True)
        estimate_tag = " (预估)" if is_estimate else ""

        # 判断是未来还是过去
        today = datetime.now().date()
        status = "upcoming" if dt.date() >= today else "past"

        return {
            "ticker": ticker.upper(),
            "type": f"Earnings {timing}{estimate_tag}",
            "date": formatted_date,
            "time": formatted_time,
            "timing": timing,
            "is_estimate": is_estimate,
            "category": "Earnings",
            "status": status,
        }
    except Exception:
        pass

    return None


def get_next_earnings_date_calendar(ticker: str) -> dict | None:
    """
    从 yfinance calendar 获取 Earnings 日期（备用）
    """
    try:
        import yfinance as yf

        stock = yf.Ticker(ticker)
        calendar = stock.calendar

        if not calendar:
            return None

        earnings_dates = calendar.get("Earnings Date", [])
        if not earnings_dates:
            return None

        # 取第一个日期
        earnings_date = earnings_dates[0]
        formatted_date = earnings_date.strftime("%Y-%m-%d")

        today = datetime.now().date()
        status = "upcoming" if earnings_date >= today else "past"

        return {
            "ticker": ticker.upper(),
            "type": "Earnings (预定)",
            "date": formatted_date,
            "time": None,
            "timing": "TBD",
            "is_estimate": True,
            "category": "Earnings",
            "status": status,
        }
    except Exception:
        pass

    return None


def get_past_earnings_call_date(ticker: str) -> dict | None:
    """
    从 Motley Fool 获取最近的 Earnings Call 日期（历史）
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }

    for exchange in ["nasdaq", "nyse"]:
        quote_url = f"https://www.fool.com/quote/{exchange}/{ticker.lower()}/"
        try:
            resp = requests.get(quote_url, headers=headers, timeout=10)
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "/earnings/call-transcripts/" in href:
                    date_match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", href)
                    if date_match:
                        date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                        return {
                            "ticker": ticker.upper(),
                            "type": "Earnings Call (已发布)",
                            "date": date_str,
                            "category": "Earnings Call",
                            "status": "past",
                        }
        except requests.RequestException:
            continue

    return None


def get_all_dates_for_ticker(ticker: str) -> list[dict]:
    """获取单个股票的所有日期事件（历史 + 未来）"""
    events = []

    # 1. 未来 Earnings 日期（优先 yfinance info，备用 calendar）
    next_earnings = get_next_earnings_date_yfinance(ticker)
    if not next_earnings:
        next_earnings = get_next_earnings_date_calendar(ticker)
    if next_earnings:
        events.append(next_earnings)

    # 2. SEC 财报（历史）
    events.extend(get_sec_filing_dates(ticker))

    # 3. 过去的 Earnings Call（历史）
    past_ec = get_past_earnings_call_date(ticker)
    if past_ec:
        events.append(past_ec)

    return events


def get_calendar_data(tickers: list[str]) -> list[dict]:
    """
    获取多个股票的日历数据
    返回按日期排序的事件列表（未来的在前）
    """
    all_events = []

    for ticker in tickers:
        events = get_all_dates_for_ticker(ticker)
        all_events.extend(events)

    # 按日期排序：未来的在前（降序），同日期按 ticker 排序
    today = datetime.now().strftime("%Y-%m-%d")

    def sort_key(e):
        is_future = e["date"] >= today
        return (not is_future, e["date"] if is_future else "9999" + e["date"], e["ticker"])

    all_events.sort(key=lambda x: (x["status"] != "upcoming", x["date"]), reverse=False)

    # 重新排序：upcoming 在前按日期升序，past 在后按日期降序
    upcoming = [e for e in all_events if e.get("status") == "upcoming"]
    past = [e for e in all_events if e.get("status") != "upcoming"]

    upcoming.sort(key=lambda x: x["date"])  # 最近的未来日期在前
    past.sort(key=lambda x: x["date"], reverse=True)  # 最近的过去日期在前

    return upcoming + past


def group_events_by_date(events: list[dict]) -> dict[str, list[dict]]:
    """按日期分组事件"""
    grouped = {}
    for event in events:
        date = event["date"]
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(event)
    return grouped


def group_events_by_month(events: list[dict]) -> dict[str, list[dict]]:
    """按月份分组事件"""
    grouped = {}
    for event in events:
        month = event["date"][:7]  # "2024-10"
        if month not in grouped:
            grouped[month] = []
        grouped[month].append(event)
    return grouped


def separate_upcoming_and_past(events: list[dict]) -> tuple[list[dict], list[dict]]:
    """分离未来和过去的事件"""
    upcoming = [e for e in events if e.get("status") == "upcoming"]
    past = [e for e in events if e.get("status") != "upcoming"]
    return upcoming, past


if __name__ == "__main__":
    # 测试
    import sys

    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL"]
    print(f"获取 {tickers} 的日历数据...\n")

    events = get_calendar_data(tickers)

    upcoming, past = separate_upcoming_and_past(events)

    if upcoming:
        print("📅 即将到来:")
        for e in upcoming:
            time_str = e.get("time", "")
            if time_str:
                print(f"  {e['date']} {time_str} | {e['ticker']:5} | {e['type']}")
            else:
                print(f"  {e['date']}       | {e['ticker']:5} | {e['type']}")

    if past:
        print("\n📜 历史记录:")
        for e in past[:10]:  # 只显示最近10条
            print(f"  {e['date']}       | {e['ticker']:5} | {e['type']}")
