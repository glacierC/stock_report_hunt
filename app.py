#!/usr/bin/env python3
"""
Stock Report Hunter - Web UI
使用 Streamlit 构建的本地网页界面
"""

import os
from pathlib import Path

import streamlit as st

from ticker_lookup import search_ticker, get_ticker
from earnings import download_earnings_transcript, search_transcript_from_quote_page, search_transcript_from_index, download_transcript_page
from main import get_cik, get_latest_filing, download_primary_document, html_to_markdown

# 配置
DOWNLOAD_DIR = Path("downloads")


def download_sec_filing(ticker: str) -> dict:
    """下载 SEC 财报，返回结果信息"""
    result = {
        "success": False,
        "files": [],
        "error": None,
    }

    try:
        cik = get_cik(ticker)
        ticker_dir = DOWNLOAD_DIR / ticker
        ticker_dir.mkdir(parents=True, exist_ok=True)

        for form_type in ["10-K", "10-Q"]:
            filing = get_latest_filing(cik, form_type)
            if not filing:
                continue

            html_content = download_primary_document(cik, filing)
            markdown = html_to_markdown(html_content)

            output_file = ticker_dir / f"{ticker}_{form_type}_{filing['filing_date']}.md"
            output_file.write_text(markdown, encoding="utf-8")

            result["files"].append({
                "type": form_type,
                "date": filing["filing_date"],
                "path": str(output_file),
                "filename": output_file.name,
            })

        result["success"] = True
    except Exception as e:
        result["error"] = str(e)

    return result


def download_earnings(ticker: str) -> dict:
    """下载 Earnings Call，返回结果信息"""
    result = {
        "success": False,
        "file": None,
        "error": None,
    }

    try:
        # 查找 transcript URL
        url = search_transcript_from_quote_page(ticker)
        if not url:
            url = search_transcript_from_index(ticker)

        if not url:
            result["error"] = f"未找到 {ticker} 的 Earnings Call Transcript"
            return result

        # 下载并解析
        content, metadata = download_transcript_page(url)
        if not content:
            result["error"] = "无法解析 Transcript 内容"
            return result

        # 保存文件
        ticker_dir = DOWNLOAD_DIR / ticker
        ticker_dir.mkdir(parents=True, exist_ok=True)

        title = metadata.get("title", f"{ticker} Earnings Call")
        date_str = metadata.get("date", "unknown")

        markdown = f"""# {title}

**Date**: {date_str}
**Source**: [Motley Fool]({url})

---

{content}
"""
        safe_date = date_str.replace("-", "")
        output_file = ticker_dir / f"{ticker}_earnings_{safe_date}.md"
        output_file.write_text(markdown, encoding="utf-8")

        result["success"] = True
        result["file"] = {
            "type": "Earnings Call",
            "date": date_str,
            "path": str(output_file),
            "filename": output_file.name,
        }
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    st.set_page_config(
        page_title="Stock Report Hunter",
        page_icon="📈",
        layout="centered",
    )

    st.title("📈 Stock Report Hunter")
    st.caption("自动下载美股财报和 Earnings Call Transcript")

    # 输入区
    col1, col2 = st.columns([3, 1])

    with col1:
        query = st.text_input(
            "输入股票代码或公司名称",
            placeholder="例如: AAPL, Apple, NVDA, Nvidia",
            key="query_input",
        )

    # 模糊匹配提示
    if query and len(query) >= 2:
        matches = search_ticker(query, limit=5)
        if matches:
            ticker = matches[0]["ticker"]

            # 如果不是精确匹配，显示候选
            if query.upper() != ticker:
                st.info(f"🔍 匹配到: **{ticker}** - {matches[0]['name']}")

                if len(matches) > 1:
                    with st.expander("其他匹配结果"):
                        for m in matches[1:]:
                            st.write(f"- **{m['ticker']}** - {m['name']}")
        else:
            ticker = None
            st.warning("未找到匹配的公司")
    else:
        ticker = None

    # 下载选项
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        download_sec = st.checkbox("SEC 财报 (10-K/10-Q)", value=True)
    with col2:
        download_ec = st.checkbox("Earnings Call", value=True)

    # 下载按钮
    if st.button("📥 开始下载", type="primary", disabled=not ticker):
        if not ticker:
            st.error("请输入有效的股票代码或公司名称")
            return

        st.markdown("---")
        st.subheader(f"📊 {ticker} 下载结果")

        # SEC 财报
        if download_sec:
            with st.spinner(f"正在下载 {ticker} SEC 财报..."):
                sec_result = download_sec_filing(ticker)

            if sec_result["success"] and sec_result["files"]:
                st.success("✅ SEC 财报下载完成")
                for f in sec_result["files"]:
                    st.markdown(f"- **{f['type']}** ({f['date']}): `{f['filename']}`")
            elif sec_result["error"]:
                st.error(f"❌ SEC 财报下载失败: {sec_result['error']}")
            else:
                st.warning("⚠️ 未找到 SEC 财报")

        # Earnings Call
        if download_ec:
            with st.spinner(f"正在下载 {ticker} Earnings Call..."):
                ec_result = download_earnings(ticker)

            if ec_result["success"] and ec_result["file"]:
                f = ec_result["file"]
                st.success("✅ Earnings Call 下载完成")
                st.markdown(f"- **{f['type']}** ({f['date']}): `{f['filename']}`")
            elif ec_result["error"]:
                st.error(f"❌ Earnings Call 下载失败: {ec_result['error']}")

        # 显示文件夹路径
        folder_path = DOWNLOAD_DIR / ticker
        if folder_path.exists():
            st.markdown("---")
            st.info(f"📁 文件保存位置: `{folder_path.absolute()}`")

            # 列出所有文件
            files = list(folder_path.glob("*.md"))
            if files:
                with st.expander("查看所有已下载文件"):
                    for f in sorted(files, reverse=True):
                        st.write(f"- {f.name}")


if __name__ == "__main__":
    main()
