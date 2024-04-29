import warnings
import pandas as pd

from datetime import datetime

warnings.filterwarnings("ignore")


class Parser:
    CURRENCIES = dict(
        DOLLAR="R01235",
        EURO="R01239",
        YUAN="R01375",
        POUND="R01035"
    )
    WINLINE_TEMPLATE = (
        "https://www.cbr.ru/Queries/UniDbQuery/DownloadExcel/132934?"
        "FromDate={start_day:0>2}%2F{start_month:0>2}%2F{start_year}&"
        "ToDate={day:0>2}%2F{month:0>2}%2F{year}&posted=False"
    )
    CURRENCY_TEMPLATE = (
        "https://www.cbr.ru/Queries/UniDbQuery/DownloadExcel/98956?Posted=True&"
        "so=1&mode=1&VAL_NM_RQ={code}&"
        "From={start_date}&To={day:0>2}.{month:0>2}.{year}&"
        "FromDate={start_day:0>2}%2F{start_month:0>2}%2F{start_year}&"
        "ToDate={day:0>2}%2F{month:0>2}%2F{year}"
    )

    def __init__(self):
        self.rate = pd.DataFrame()
        self.currencies = pd.DataFrame(columns=["data", "curs", "cdx"])

    @staticmethod
    def replace_cdx(cdx):
        if cdx == "Доллар США":
            return "dollar"
        elif cdx == "Китайский юань":
            return "yuan"
        elif cdx == "Евро":
            return "euro"
        return "pound"

    def get_rate(self, date: str = "01.07.2014"):
        start_day, start_month, start_year = map(int, date.split("."))
        url = self.WINLINE_TEMPLATE.format(
            day=datetime.now().day,
            month=datetime.now().month,
            year=datetime.now().year,
            start_day=start_day,
            start_month=start_month,
            start_year=start_year
        )
        self.rate = pd.read_excel(url)

        print("RATE PARSED")

    def get_currencies(self, date: str = "01.07.2014"):
        start_day, start_month, start_year = map(int, date.split("."))
        for wallet, code in self.CURRENCIES.items():
            url = self.CURRENCY_TEMPLATE.format(
                day=datetime.now().day,
                month=datetime.now().month,
                year=datetime.now().year,
                code=code,
                start_day=start_day,
                start_month=start_month,
                start_year=start_year,
                start_date=date
            )
            wallet_rate = pd.read_excel(url)
            self.currencies = pd.concat([self.currencies, wallet_rate.drop("nominal", axis=1)])
            print(f"{wallet} PARSED")

    def get_data(self, date: str = "01.07.2014"):
        self.get_rate(date)
        self.get_currencies(date)
        currencies = self.currencies.copy()
        currencies.cdx = currencies.cdx.apply(self.replace_cdx)
        currencies.data = currencies.data.apply(str)

        dollar = currencies.loc[currencies.cdx == "dollar"]
        euro = currencies.loc[currencies.cdx == "euro"]
        yuan = currencies.loc[currencies.cdx == "yuan"]
        pound = currencies.loc[currencies.cdx == "pound"]

        dollar["date2"] = dollar.data.apply(lambda x: "-".join(x.split("-")[:-1]))
        dollar = dollar.rename(columns={"curs": "dollar_curs"})

        euro["date2"] = euro.data.apply(lambda x: "-".join(x.split("-")[:-1]))
        euro = euro.rename(columns={"curs": "euro_curs"})

        yuan["date2"] = yuan.data.apply(lambda x: "-".join(x.split("-")[:-1]))
        yuan = yuan.rename(columns={"curs": "yuan_curs"})

        pound["date2"] = pound.data.apply(lambda x: "-".join(x.split("-")[:-1]))
        pound = pound.rename(columns={"curs": "pound_curs"})

        rate = self.rate.rename(columns={
            "Дата": "date2",
            "Ключевая ставка, % годовых": "rate",
            "Инфляция, % г/г": "inflation"
        })
        rate = rate.drop(["Цель по инфляции"], axis=1)

        rate.date2 = rate.date2.apply(lambda x: "{}-{:0>2}".format(*str(x).split(".")[::-1]))
        data = dollar[["dollar_curs", "date2", "data"]].merge(rate, on="date2")
        data = data.merge(euro[["euro_curs", "date2"]], on="date2")
        data = data.merge(pound[["pound_curs", "date2"]], on="date2")
        data = data.merge(yuan[["yuan_curs", "date2"]], on="date2")
        # data = data.drop("date2", axis=1)
        data = data.drop_duplicates(subset=['data'], keep='first')
        return data