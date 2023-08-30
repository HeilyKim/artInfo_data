import pandas as pd
def getDates(date_range):
    date_range = date_range.split(" / ")[0]
    start_date, end_date = date_range.split(" ▶ ")
    start_date = pd.to_datetime(start_date, format="%Y_%m%d").strftime("%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y_%m%d").strftime("%Y-%m-%d")
    return start_date, end_date

def getDateForContest(df, col):
    df['start_date'] = df[col].apply(lambda x: x.replace('접수기간 / ', '').split(' ▶ ')[0])
    df['end_date'] = df[col].apply(lambda x: x.replace('접수기간 / ', '').split(' ▶ ')[1])
    df['start_date'] = pd.to_datetime(df['start_date'], format="%Y_%m%d").dt.strftime("%Y-%m-%d")
    df['end_date'] = pd.to_datetime(df['end_date'], format="%Y_%m%d").dt.strftime("%Y-%m-%d")
    df.drop(col, axis=1, inplace=True)
    print(df['start_date'][0])
    print(df['end_date'][0])
    return df

def cleaned(text):
    return text.replace("●", "\n●")
