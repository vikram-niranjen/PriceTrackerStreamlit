import streamlit as st
import requests
from datetime import datetime
import pandas as pd





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
        temp["datetime"] = datetime.fromtimestamp(int(record["RowKey"]))
        price_history_records.append(temp)
    price_history_records = pd.DataFrame(price_history_records)
    st.line_chart(data=price_history_records,  x="datetime", y="Price", )



