import streamlit as st
import requests
import pandas as pd
import datetime

st.title('주식 차트')

with st.sidebar:
    sdt = st.date_input(
        "조회 시작일을 선택해 주세요",
        datetime.datetime(2024, 1, 1)
    )

    edt = st.date_input(
        "조회 종료일을 선택해 주세요",
        datetime.datetime(2024, 1, 1)
    )

    code = st.text_input(
        '종목코드', 
        value='',
        placeholder='종목코드를 입력해 주세요'
    )

def get_stockprice(code, sdt, edt) :
  URL = "https://m.stock.naver.com/front-api/external/chart/domestic/info?symbol={0}&requestType=1&startTime={1}&endTime={2}&timeframe=day".format(code, sdt, edt)
  print(URL)
  res = requests.get(URL)
  li = eval(res.text.replace("\n","").replace("\t",""))
  return pd.DataFrame(columns=li[0],data=li[1:])


if code and sdt and edt:

    df = get_stockprice(code, sdt.strftime("%Y%m%d"), edt.strftime("%Y%m%d"))
    data = df.sort_index(ascending=True).loc[:, '종가']
    st.line_chart(data)
    vol_data = df.sort_index(ascending=True).loc[:, '거래량']
    st.bar_chart(vol_data)
    # 다운로드 버튼 연결
    st.download_button(
        label='CSV로 다운로드',
        data=df.to_csv(), 
        file_name='{0}.csv'.format(code), 
        mime='text/csv'
    )
    st.dataframe(df)