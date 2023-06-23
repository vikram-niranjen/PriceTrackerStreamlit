import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import copy





params = st.experimental_get_query_params()
if "product_id" in params:
    st.title("PriceTracker")
    product_id = params["product_id"][0]
    response = requests.get(f"https://cs-price-tracker-jobs.azurewebsites.net/api/ProductHistory?productid={product_id}")
    records = response.json()
    price_history_records = []
    for record in records:
        temp = {}
        temp["Price"] = record["Price"]
        temp["DateTime"] = datetime.fromtimestamp(int(record["RowKey"]))
        price_history_records.append(temp)
    price_history_records = pd.DataFrame(price_history_records)

    min_date = price_history_records["DateTime"].min()
    max_date = price_history_records["DateTime"].max()


    start_date = copy.deepcopy(min_date)
    end_date = copy.deepcopy(max_date)

    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Start Date",  value =min_date, min_value=min_date)

    with date_col2:
        end_date = st.date_input("End Date",  value= max_date,max_value=max_date)


    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)


    filtered = price_history_records.loc[(price_history_records["DateTime"]>=start_date)&(price_history_records["DateTime"]<=end_date)]
    st.line_chart(data=filtered,  x="DateTime", y="Price", )



