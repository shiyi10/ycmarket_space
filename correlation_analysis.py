import pandas as pd


# ==========================
# 读取Excel
# ==========================
space_df = pd.read_excel(
    "云创矩阵分析.xlsx",
    sheet_name="竞价空间"
)

price_df = pd.read_excel(
    "云创矩阵分析.xlsx",
    sheet_name="日前价格"
)

# 第一列是日期
time_cols = list(space_df.columns[1:])

results = []

# ==========================
# 每个时刻分别计算
# ==========================
for t in time_cols:

    try:

        space = pd.to_numeric(
            space_df[t],
            errors="coerce"
        )

        price = pd.to_numeric(
            price_df[t],
            errors="coerce"
        )

        corr = space.corr(price)

        results.append({
            "时刻": t,
            "相关系数": corr
        })

    except Exception as e:

        print(t, e)

# ==========================
# 保存结果
# ==========================
result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    by="相关系数"
)

print(result_df)

result_df.to_excel(
    "时刻相关性分析.xlsx",
    index=False
)

print("\n✅ 已生成：时刻相关性分析.xlsx")