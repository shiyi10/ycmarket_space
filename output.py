from ycmarket_analyse import WindowSpaceAnalyzer


if __name__ == "__main__":

    analyzer = WindowSpaceAnalyzer(
        "云创矩阵分析.xlsx"
    )

    result = analyzer.full_analysis(
        target_time="14:00",
        target_space=70000,
        topk=20
    )

    print("\n========================")
    print("Top20结果")
    print("========================")

    print(
        result["topk"]
    )

    print("\n========================")
    print("价格统计")
    print("========================")

    for k, v in result["stats"].items():

        print(
            f"{k}: {v}"
        )

    print("\n========================")
    print("KNN预测价格")
    print("========================")

    print(
        result["pred_price"]
    )