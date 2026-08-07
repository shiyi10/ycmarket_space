import pandas as pd


class WindowSpaceAnalyzer:

    def __init__(self, excel_path):

        # ==========================
        # 读取两个Sheet
        # ==========================
        self.space_df = pd.read_excel(
            excel_path,
            sheet_name="竞价空间"
        )

        self.price_df = pd.read_excel(
            excel_path,
            sheet_name="日前价格"
        )

        # 第一列统一改名
        self.space_df.rename(
            columns={
                self.space_df.columns[0]: "日期"
            },
            inplace=True
        )

        self.price_df.rename(
            columns={
                self.price_df.columns[0]: "日期"
            },
            inplace=True
        )

        # ==========================
        # 时间列
        # ==========================
        self.time_cols = list(
            self.space_df.columns[1:]
        )

        print(
            f"读取完成，共 {len(self.time_cols)} 个时段"
        )

    # =====================================
    # 获取相邻时间
    # =====================================
    def get_neighbor_times(
            self,
            target_time
    ):

        if target_time not in self.time_cols:
            raise ValueError(
                f"时间不存在: {target_time}"
            )

        idx = self.time_cols.index(
            target_time
        )

        result = []

        if idx > 0:
            result.append(
                self.time_cols[idx - 1]
            )

        result.append(
            self.time_cols[idx]
        )

        if idx < len(self.time_cols) - 1:
            result.append(
                self.time_cols[idx + 1]
            )

        return result

    # =====================================
    # TopK最近样本
    # =====================================
    def find_window_closest(
            self,
            target_time,
            target_space,
            topk=20
    ):

        neighbor_times = self.get_neighbor_times(
            target_time
        )

        print(
            "查询窗口:",
            neighbor_times
        )

        rows = []

        # =====================================
        # 遍历全部日期
        # =====================================
        for row_idx in range(
                len(self.space_df)
        ):

            date = self.space_df.loc[
                row_idx,
                "日期"
            ]

            for t in neighbor_times:

                try:

                    bidding_space = float(
                        self.space_df.loc[
                            row_idx,
                            t
                        ]
                    )

                    day_price = float(
                        self.price_df.loc[
                            row_idx,
                            t
                        ]
                    )

                    diff = abs(
                        bidding_space
                        - target_space
                    )

                    rows.append({
                        "日期": date,
                        "时刻": t,
                        "竞价空间": bidding_space,
                        "日前价格": day_price,
                        "误差": diff
                    })

                except:
                    continue

        result = pd.DataFrame(rows)

        if result.empty:
            return result

        result = result.sort_values(
            by="误差"
        )

        result = result.head(topk)

        return result.reset_index(
            drop=True
        )

    # =====================================
    # 价格统计分析
    # =====================================
    def analyze_price_distribution(
            self,
            result_df
    ):

        if result_df.empty:
            return {}

        prices = result_df["日前价格"]

        stats = {

            "样本数":
                len(prices),

            "平均价格":
                round(
                    prices.mean(),
                    2
                ),

            "中位数":
                round(
                    prices.median(),
                    2
                ),

            "P10":
                round(
                    prices.quantile(0.10),
                    2
                ),

            "P25":
                round(
                    prices.quantile(0.25),
                    2
                ),

            "P75":
                round(
                    prices.quantile(0.75),
                    2
                ),

            "P90":
                round(
                    prices.quantile(0.90),
                    2
                ),

            "最大价格":
                round(
                    prices.max(),
                    2
                ),

            "最小价格":
                round(
                    prices.min(),
                    2
                )
        }

        return stats

    # =====================================
    # KNN加权预测价格
    # =====================================
    def predict_price_knn(
            self,
            result_df
    ):

        if result_df.empty:
            return None

        eps = 1e-6

        weights = (
                1 /
                (
                        result_df["误差"]
                        + eps
                )
        )

        pred_price = (
                (
                        result_df["日前价格"]
                        * weights
                ).sum()
                /
                weights.sum()
        )

        return round(
            pred_price,
            2
        )

    # =====================================
    # 一键分析
    # =====================================
    def full_analysis(
            self,
            target_time,
            target_space,
            topk=20
    ):

        result = self.find_window_closest(
            target_time,
            target_space,
            topk
        )

        stats = self.analyze_price_distribution(
            result
        )

        pred_price = self.predict_price_knn(
            result
        )

        return {
            "topk": result,
            "stats": stats,
            "pred_price": pred_price,

            "p10": stats["P10"],
            "p25": stats["P25"],
            "p50": stats["中位数"],
            "p75": stats["P75"],
            "p90": stats["P90"]
        }