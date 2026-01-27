#!/usr/bin/env python3
"""
财报下载工具 v0.3 - 下载SEC财报和Earnings Call Transcript
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


# SEC API 要求设置 User-Agent
HEADERS = {
    "User-Agent": os.environ.get("SEC_USER_AGENT", "MyApp contact@example.com"),
    "Accept-Encoding": "gzip, deflate",
}


def get_cik(ticker: str) -> str:
    """通过 ticker 获取公司 CIK"""
    url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": ticker,
        "type": "10-K",
        "dateb": "",
        "owner": "include",
        "count": 1,
        "output": "atom",
    }
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()

    # 从 Atom feed 中提取 CIK
    match = re.search(r"CIK=(\d+)", resp.text)
    if not match:
        raise ValueError(f"无法找到 {ticker} 的 CIK")
    return match.group(1)


def get_latest_filing(cik: str, form_type: str) -> dict | None:
    """获取最新的指定类型 filing 信息"""
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()

    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    accessions = filings.get("accessionNumber", [])
    primary_docs = filings.get("primaryDocument", [])
    filing_dates = filings.get("filingDate", [])

    for i, form in enumerate(forms):
        if form == form_type:
            return {
                "accession": accessions[i].replace("-", ""),
                "accession_display": accessions[i],
                "primary_document": primary_docs[i],
                "filing_date": filing_dates[i],
            }
    return None


def download_primary_document(cik: str, filing: dict) -> str:
    """下载主文档 HTML 内容"""
    accession = filing["accession"]
    primary_doc = filing["primary_document"]

    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{primary_doc}"
    print(f"  下载: {url}")

    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.text


def html_to_markdown(html_content: str) -> str:
    """将 HTML 转换为干净的 Markdown"""
    soup = BeautifulSoup(html_content, "html.parser")

    # 移除不需要的元素
    for tag in soup.find_all(["script", "style", "meta", "link", "noscript"]):
        tag.decompose()

    # 移除隐藏元素
    for tag in soup.find_all(style=re.compile(r"display:\s*none", re.I)):
        tag.decompose()

    # 转换为 Markdown
    markdown = md(str(soup), heading_style="ATX", bullets="-")

    # 清理多余空行
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()


def download_and_convert(ticker: str, download_dir: Path) -> tuple[Path, list[dict]]:
    """下载并转换财报，返回 (目录路径, 文件信息列表)"""
    print(f"正在处理 {ticker}...")

    # 获取 CIK
    print("  获取公司 CIK...")
    cik = get_cik(ticker)
    print(f"  CIK: {cik}")

    # 创建下载目录
    ticker_dir = download_dir / ticker
    ticker_dir.mkdir(parents=True, exist_ok=True)

    downloaded_files = []

    # 尝试获取 10-K 和 10-Q
    for form_type in ["10-K", "10-Q"]:
        print(f"  查找最新 {form_type}...")
        filing = get_latest_filing(cik, form_type)

        if not filing:
            print(f"  未找到 {form_type}")
            continue

        print(f"  找到 {form_type} ({filing['filing_date']})")

        # 下载主文档
        html_content = download_primary_document(cik, filing)

        # 转换为 Markdown
        print("  转换为 Markdown...")
        markdown = html_to_markdown(html_content)

        # 保存文件
        output_file = ticker_dir / f"{ticker}_{form_type}_{filing['filing_date']}.md"
        output_file.write_text(markdown, encoding="utf-8")
        print(f"  已保存: {output_file.name}")

        downloaded_files.append({
            "type": form_type,
            "date": filing["filing_date"],
            "filename": output_file.name,
        })

    return ticker_dir, downloaded_files


def open_folder(folder_path: Path) -> None:
    """打开文件夹 (macOS)"""
    if folder_path.exists():
        subprocess.run(["open", str(folder_path)])
        print(f"\n已打开文件夹: {folder_path}")
    else:
        print(f"\n警告: 文件夹不存在 {folder_path}")


def show_prompt() -> None:
    """显示 my_prompt.txt 的内容"""
    prompt_file = Path("my_prompt.txt")
    if prompt_file.exists():
        print("\n" + "=" * 50)
        print("分析提示:")
        print("=" * 50)
        print(prompt_file.read_text())
    else:
        print("\n提示: 未找到 my_prompt.txt 文件")


def print_report_summary(sec_files: list[dict], earnings_date: str | None):
    """打印报告时间摘要"""
    print("\n" + "=" * 50)
    print("📅 报告时间摘要")
    print("=" * 50)

    if sec_files:
        for f in sec_files:
            print(f"  {f['type']:6} 发布日期: {f['date']}")

    if earnings_date:
        print(f"  Earnings Call 日期: {earnings_date}")

    if not sec_files and not earnings_date:
        print("  (无报告信息)")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="下载SEC财报和Earnings Call")
    parser.add_argument("ticker", help="股票代码 (如 NVDA, AAPL)")
    parser.add_argument("--earnings", "-e", action="store_true",
                        help="下载 Earnings Call Transcript")
    parser.add_argument("--no-sec", action="store_true",
                        help="跳过 SEC 财报下载")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    download_dir = Path("downloads")
    ticker_folder = download_dir / ticker

    sec_files = []
    earnings_date = None

    try:
        # 下载 SEC 财报 (10-K, 10-Q)
        if not args.no_sec:
            ticker_folder, sec_files = download_and_convert(ticker, download_dir)

        # 下载 Earnings Call Transcript
        if args.earnings:
            from earnings import download_earnings_transcript, search_transcript_from_quote_page, search_transcript_from_index, download_transcript_page

            # 获取日期信息
            url = search_transcript_from_quote_page(ticker)
            if not url:
                url = search_transcript_from_index(ticker)
            if url:
                _, metadata = download_transcript_page(url)
                earnings_date = metadata.get("date")

            ticker_folder = download_earnings_transcript(ticker, download_dir)

        # 打印报告时间摘要
        print_report_summary(sec_files, earnings_date)

        open_folder(ticker_folder)
        show_prompt()
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
