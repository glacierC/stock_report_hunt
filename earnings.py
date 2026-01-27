#!/usr/bin/env python3
"""
Earnings Call Transcript 下载模块
数据源: The Motley Fool (免费爬取)
"""

import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
}


def search_transcript_from_quote_page(ticker: str) -> str | None:
    """从 Motley Fool 的公司 quote 页面查找 transcript 链接"""
    # 尝试 NASDAQ 和 NYSE
    for exchange in ["nasdaq", "nyse"]:
        quote_url = f"https://www.fool.com/quote/{exchange}/{ticker.lower()}/"

        try:
            resp = requests.get(quote_url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # 查找 transcript 链接
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "/earnings/call-transcripts/" in href:
                    if href.startswith("/"):
                        return f"https://www.fool.com{href}"
                    return href
        except requests.RequestException:
            continue

    return None


def search_transcript_from_index(ticker: str) -> str | None:
    """从 Motley Fool 的 transcript 索引页面查找"""
    index_url = "https://www.fool.com/earnings-call-transcripts/"

    resp = requests.get(index_url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # 查找包含 ticker 的链接
    ticker_lower = ticker.lower()
    for link in soup.find_all("a", href=True):
        href = link["href"]
        text = link.get_text().lower()
        if "/earnings/call-transcripts/" in href:
            # 检查链接文本或 URL 中是否包含 ticker
            if f"({ticker_lower})" in text or f"-{ticker_lower}-" in href.lower():
                if href.startswith("/"):
                    return f"https://www.fool.com{href}"
                return href

    return None


def download_transcript_page(url: str) -> tuple[str, dict]:
    """下载并解析 transcript 页面"""
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # 提取标题
    title = ""
    title_tag = soup.find("h1")
    if title_tag:
        title = title_tag.get_text().strip()

    # 提取日期 (从 URL 或页面)
    date_match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
    date_str = ""
    if date_match:
        date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"

    # 提取 transcript 内容
    # Motley Fool 的 transcript 通常在 article-body 或 content 区域
    content = ""

    # 尝试多种选择器
    article = soup.find("article") or soup.find("div", class_="article-body") or soup.find("div", class_="content")

    if article:
        # 移除不需要的元素
        for tag in article.find_all(["script", "style", "nav", "aside", "footer"]):
            tag.decompose()

        # 转换为 Markdown
        content = md(str(article), heading_style="ATX", bullets="-")
        content = re.sub(r"\n{3,}", "\n\n", content)

    metadata = {
        "title": title,
        "date": date_str,
        "url": url,
    }

    return content.strip(), metadata


def download_earnings_transcript(ticker: str, download_dir: Path) -> Path:
    """下载最新的 Earnings Call Transcript"""
    print(f"正在获取 {ticker} 的 Earnings Call...")

    # 先从公司 quote 页面找
    print("  搜索 Motley Fool...")
    url = search_transcript_from_quote_page(ticker)

    # 如果没找到，尝试索引页
    if not url:
        print("  Quote 页面未找到，尝试索引页...")
        url = search_transcript_from_index(ticker)

    if not url:
        raise ValueError(f"未找到 {ticker} 的 Earnings Call Transcript")

    print(f"  找到: {url}")

    # 下载并解析
    print("  下载 Transcript...")
    content, metadata = download_transcript_page(url)

    if not content:
        raise ValueError("无法解析 Transcript 内容")

    # 创建目录
    ticker_dir = download_dir / ticker
    ticker_dir.mkdir(parents=True, exist_ok=True)

    # 构建 Markdown
    title = metadata.get("title", f"{ticker} Earnings Call")
    date_str = metadata.get("date", "unknown")

    markdown = f"""# {title}

**Date**: {date_str}
**Source**: [Motley Fool]({url})

---

{content}
"""

    # 生成文件名
    safe_date = date_str.replace("-", "")
    output_file = ticker_dir / f"{ticker}_earnings_{safe_date}.md"
    output_file.write_text(markdown, encoding="utf-8")
    print(f"  已保存: {output_file.name}")

    return ticker_dir


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ticker = sys.argv[1].upper()
        download_earnings_transcript(ticker, Path("downloads"))
