#!/usr/bin/env python3
"""
Stock Report Hunter - Web UI
使用 Streamlit 构建的本地网页界面
"""

from pathlib import Path

import streamlit as st

from ticker_lookup import search_ticker
from earnings import search_transcript_from_quote_page, search_transcript_from_index, download_transcript_page
from main import get_cik, get_latest_filing, download_primary_document, html_to_markdown
from watchlist import load_watchlist, add_to_watchlist, remove_from_watchlist
from calendar_data import get_calendar_data, group_events_by_month, separate_upcoming_and_past

# 配置
DOWNLOAD_DIR = Path("downloads")


def download_sec_filing(ticker: str) -> dict:
    """下载 SEC 财报，返回结果信息"""
    result = {"success": False, "files": [], "error": None}

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
    result = {"success": False, "file": None, "error": None}

    try:
        url = search_transcript_from_quote_page(ticker)
        if not url:
            url = search_transcript_from_index(ticker)

        if not url:
            result["error"] = f"未找到 {ticker} 的 Earnings Call Transcript"
            return result

        content, metadata = download_transcript_page(url)
        if not content:
            result["error"] = "无法解析 Transcript 内容"
            return result

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


def download_all_for_ticker(ticker: str, download_sec: bool = True, download_ec: bool = True) -> dict:
    """下载单个股票的所有资料"""
    results = {"ticker": ticker, "sec": None, "earnings": None}

    if download_sec:
        results["sec"] = download_sec_filing(ticker)
    if download_ec:
        results["earnings"] = download_earnings(ticker)

    return results


# ============== 页面: 单股票查询 ==============
def page_single_search():
    st.header("🔍 单股票查询")

    query = st.text_input(
        "输入股票代码或公司名称",
        placeholder="例如: AAPL, Apple, NVDA, Nvidia",
        key="query_input",
    )

    ticker = None
    if query and len(query) >= 2:
        matches = search_ticker(query, limit=5)
        if matches:
            ticker = matches[0]["ticker"]
            if query.upper() != ticker:
                st.info(f"🔍 匹配到: **{ticker}** - {matches[0]['name']}")
                if len(matches) > 1:
                    with st.expander("其他匹配结果"):
                        for m in matches[1:]:
                            st.write(f"- **{m['ticker']}** - {m['name']}")
        else:
            st.warning("未找到匹配的公司")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        download_sec = st.checkbox("SEC 财报 (10-K/10-Q)", value=True)
    with col2:
        download_ec = st.checkbox("Earnings Call", value=True)
    with col3:
        add_watch = st.checkbox("添加到 Watchlist", value=False)

    if st.button("📥 开始下载", type="primary", disabled=not ticker):
        if add_watch and ticker:
            add_to_watchlist(ticker)
            st.toast(f"已添加 {ticker} 到 Watchlist")

        st.markdown("---")
        st.subheader(f"📊 {ticker} 下载结果")

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

        if download_ec:
            with st.spinner(f"正在下载 {ticker} Earnings Call..."):
                ec_result = download_earnings(ticker)

            if ec_result["success"] and ec_result["file"]:
                f = ec_result["file"]
                st.success("✅ Earnings Call 下载完成")
                st.markdown(f"- **{f['type']}** ({f['date']}): `{f['filename']}`")
            elif ec_result["error"]:
                st.error(f"❌ Earnings Call 下载失败: {ec_result['error']}")

        folder_path = DOWNLOAD_DIR / ticker
        if folder_path.exists():
            st.markdown("---")
            st.info(f"📁 文件保存位置: `{folder_path.absolute()}`")


# ============== 页面: 日历视图 ==============
def page_calendar():
    st.header("📅 财报日历")

    watchlist = load_watchlist()

    if not watchlist:
        st.warning("Watchlist 为空，请先添加股票")
        st.info("在「单股票查询」页面下载时勾选「添加到 Watchlist」，或在侧边栏手动添加")
        return

    st.write(f"当前关注: **{', '.join(watchlist)}**")

    # 获取日历数据
    with st.spinner("正在获取财报日期（包含未来预定）..."):
        events = get_calendar_data(watchlist)

    if not events:
        st.warning("未找到任何财报日期信息")
        return

    # 分离未来和过去的事件
    upcoming, past = separate_upcoming_and_past(events)

    # 显示即将到来的事件（重点）
    st.subheader("🔮 即将到来")
    if upcoming:
        table_data = []
        for e in upcoming:
            time_str = e.get("time", "")
            date_display = f"{e['date']} {time_str}" if time_str else e["date"]
            table_data.append({
                "日期时间": date_display,
                "股票": e["ticker"],
                "类型": e["type"],
            })
        st.table(table_data)
    else:
        st.info("暂无已确定的未来财报日期")

    # 显示历史记录（折叠）
    st.subheader("📜 历史记录")
    if past:
        by_month = group_events_by_month(past)
        for month, month_events in sorted(by_month.items(), reverse=True)[:3]:  # 只显示最近3个月
            with st.expander(f"📆 {month}"):
                table_data = []
                for e in sorted(month_events, key=lambda x: x["date"], reverse=True):
                    table_data.append({
                        "日期": e["date"],
                        "股票": e["ticker"],
                        "类型": e["type"],
                    })
                st.table(table_data)
    else:
        st.info("暂无历史记录")

    # 批量下载
    st.markdown("---")
    st.subheader("📥 批量下载")

    col1, col2 = st.columns(2)
    with col1:
        batch_sec = st.checkbox("SEC 财报", value=True, key="batch_sec")
    with col2:
        batch_ec = st.checkbox("Earnings Call", value=True, key="batch_ec")

    if st.button("📥 下载全部 Watchlist", type="primary"):
        progress = st.progress(0)
        status = st.empty()

        for i, ticker in enumerate(watchlist):
            status.write(f"正在下载 {ticker}...")
            download_all_for_ticker(ticker, batch_sec, batch_ec)
            progress.progress((i + 1) / len(watchlist))

        status.empty()
        progress.empty()
        st.success(f"✅ 已下载 {len(watchlist)} 只股票的资料")
        st.info(f"📁 文件保存位置: `{DOWNLOAD_DIR.absolute()}`")


# ============== 侧边栏: Watchlist 管理 ==============
def sidebar_watchlist():
    st.sidebar.header("📋 Watchlist")

    watchlist = load_watchlist()

    if watchlist:
        for ticker in watchlist:
            col1, col2 = st.sidebar.columns([3, 1])
            col1.write(ticker)
            if col2.button("❌", key=f"remove_{ticker}"):
                remove_from_watchlist(ticker)
                st.rerun()
    else:
        st.sidebar.write("_(空)_")

    # 添加新股票
    st.sidebar.markdown("---")
    new_ticker = st.sidebar.text_input("添加股票", placeholder="输入代码", key="new_ticker")
    if st.sidebar.button("➕ 添加", key="add_btn"):
        if new_ticker:
            if add_to_watchlist(new_ticker):
                st.sidebar.success(f"已添加 {new_ticker.upper()}")
                st.rerun()
            else:
                st.sidebar.warning("已在列表中")


# ============== 主程序 ==============
def main():
    st.set_page_config(
        page_title="Stock Report Hunter",
        page_icon="📈",
        layout="wide",
    )

    st.title("📈 Stock Report Hunter")

    # 侧边栏
    sidebar_watchlist()

    # 页面导航
    tab1, tab2 = st.tabs(["🔍 单股票查询", "📅 财报日历"])

    with tab1:
        page_single_search()

    with tab2:
        page_calendar()


if __name__ == "__main__":
    main()
