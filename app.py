import streamlit as st
import pandas as pd
import plotly.express as px

from ycmarket_analyse import WindowSpaceAnalyzer


# ==================================
# 页面配置
# ==================================
st.set_page_config(
    page_title="竞价空间决策系统",
    layout="wide"
)

st.title("⚡竞价空间历史样本决策系统")


# ==================================
# 缓存加载
# ==================================
@st.cache_resource
def load_analyzer():

    return WindowSpaceAnalyzer(
        "云创矩阵分析.xlsx"
    )


analyzer = load_analyzer()


# ==================================
# 输入区
# ==================================
st.sidebar.header("参数设置")

target_time = st.sidebar.selectbox(
    "目标时刻",
    analyzer.time_cols,
    index=20
)

target_space = st.sidebar.number_input(
    "目标竞价空间(MW)",
    value=70000.0,
    step=100.0
)

topk = st.sidebar.slider(
    "TopK样本数",
    min_value=5,
    max_value=50,
    value=20
)


# ==================================
# 查询按钮
# ==================================
if st.sidebar.button("开始分析"):

    result = analyzer.full_analysis(
        target_time=target_time,
        target_space=target_space,
        topk=topk
    )

    top_df = result["topk"]

    stats = result["stats"]

    pred_price = result["pred_price"]

    # ==================================
    # 第一行：预测结果
    # ==================================
    st.header("📈预测结果")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "KNN预测价格",
        f"{pred_price:.2f}"
    )

    c2.metric(
        "P25",
        f"{stats['P25']:.2f}"
    )

    c3.metric(
        "P75",
        f"{stats['P75']:.2f}"
    )

    st.info(
        f"推荐价格区间："
        f"{stats['P25']:.2f} ~ "
        f"{stats['P75']:.2f}"
    )

    # ==================================
    # 第二行：统计指标
    # ==================================
    st.header("📊价格统计")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "平均价格",
        stats["平均价格"]
    )

    col2.metric(
        "中位数(P50)",
        stats["中位数"]
    )

    col3.metric(
        "P10",
        stats["P10"]
    )

    col4.metric(
        "P90",
        stats["P90"]
    )

    # ==================================
    # Top20结果
    # ==================================
    st.header("🔍Top相似样本")

    st.dataframe(
        top_df,
        use_container_width=True,
        height=500
    )

    # ==================================
    # 分布图
    # ==================================
    st.header("📉日前价格分布")

    fig = px.histogram(
        top_df,
        x="日前价格",
        nbins=10,
        title="Top样本价格分布"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================
    # 箱线图
    # ==================================
    st.header("📦价格箱线图")

    fig2 = px.box(
        top_df,
        y="日前价格",
        points="all"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ==================================
    # 散点图
    # ==================================
    st.header("🎯竞价空间 vs 日前价格")

    fig3 = px.scatter(
        top_df,
        x="竞价空间",
        y="日前价格",
        hover_data=[
            "日期",
            "时刻"
        ],
        title="Top样本散点图"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:

    st.info(
        "请在左侧输入目标时刻和竞价空间，然后点击【开始分析】"
    )