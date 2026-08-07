import pandas as pd


def save_to_excel(data: list, filename: str):

    df = pd.DataFrame(data)

    if df.empty:
        print("❌ 无数据")
        return

    # =========================
    # 时间标准化
    # =========================
    df["time"] = df["time"].astype(str)

    # =========================
    # 竞价空间矩阵
    # =========================
    space_df = df.pivot_table(
        index="date",
        columns="time",
        values="bidding_space",
        aggfunc="mean"
    )

    # =========================
    # 日前价格矩阵
    # =========================
    price_df = df.pivot_table(
        index="date",
        columns="time",
        values="day_ahead_price",
        aggfunc="mean"
    )

    # =========================
    # 排序（关键）
    # =========================
    space_df = space_df.sort_index()
    price_df = price_df.sort_index()

    space_df = space_df.reindex(sorted(space_df.columns), axis=1)
    price_df = price_df.reindex(sorted(price_df.columns), axis=1)

    # =========================
    # 写Excel
    # =========================
    path = f"{filename}.xlsx"

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        space_df.to_excel(writer, sheet_name="竞价空间")
        price_df.to_excel(writer, sheet_name="日前价格")

    print(f"✅ 已生成矩阵Excel: {path}")