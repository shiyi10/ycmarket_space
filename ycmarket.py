import requests


class YunChuangAPI:

    def __init__(self, token: str):
        self.URL = "https://www.yunchuangenergy.com/eletrade-assist-service/assist/market-info/supply-demand/bidding-scatter"

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "authorization": f"Bearer {token}",
            "origin": "https://www.yunchuangenergy.com",
            "referer": "https://www.yunchuangenergy.com/admin2.0/market-information/grid-supply-demand",
            "user-agent": "Mozilla/5.0"
        }

    def fetch(self, start_date: str, end_date: str, province_code="33"):

        payload = {
            "provinceCode": province_code,
            "startDate": start_date,
            "endDate": end_date
        }

        resp = requests.post(
            self.URL,
            json=payload,
            headers=self.headers,
            timeout=30
        )

        print("HTTP状态码:", resp.status_code)
        resp.raise_for_status()

        data = resp.json()

        points = data.get("data", {}).get("points", [])

        result = []

        for p in points:
            try:
                result.append({
                    "date": p["date"],
                    "time": p["time"],
                    "bidding_space": float(p.get("biddingSpace", 0)),
                    "day_ahead_price": float(p.get("dayAheadPrice", 0))
                })
            except:
                continue

        return result