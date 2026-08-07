import os
from datetime import datetime

from ycmarket import YunChuangAPI
from save_excel import save_to_excel


if __name__ == "__main__":

    # =========================
    # 获取Token
    # 优先读取环境变量
    # =========================

    token = os.getenv("YC_TOKEN")


    # 如果本地没有环境变量
    # 使用你的最新Token
    if not token:

        token = "eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6Ijc4MTc2Yzc4LTU2ZTgtNDdmNi1hNGE3LTllOWVjZWE2MTFjNyJ9.2vZ9qzfXG46cq_HhQ0rad_o40YUInvLPHcVoLEkJufIuUlTx39oIbkzg86pETRHTkuug-A0S9DW2vjmrnIIUbw"


    if not token:

        raise ValueError(
            "没有找到Token"
        )


    print(
        "Token长度:",
        len(token)
    )


    # =========================
    # 创建API
    # =========================

    api = YunChuangAPI(token)


    # =========================
    # 自动获取今天日期
    # =========================

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    print(
        "开始更新数据..."
    )

    print(
        "结束日期:",
        today
    )


    # =========================
    # 请求数据
    # =========================

    data = api.fetch(

        start_date="2026-04-01",

        end_date=today

    )


    print(
        "数据量:",
        len(data)
    )


    if len(data) > 0:

        print(
            "最新记录:"
        )

        print(
            data[-1]
        )


    # =========================
    # 保存Excel
    # =========================

    save_to_excel(

        data,

        "云创矩阵分析"

    )


    print(
        "更新完成"
    )