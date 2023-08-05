import pandas as pd
def getDates(date_range):
    date_range = date_range.split(" / ")[0]
    start_date, end_date = date_range.split(" ▶ ")
    start_date = pd.to_datetime(start_date, format="%Y_%m%d").strftime("%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y_%m%d").strftime("%Y-%m-%d")
    return start_date, end_date


def cleaned(text):
    return text.replace("●", "\n●")
