import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent.parent
st.set_page_config(page_title="Used Car Price Estimator", page_icon="🚗", layout="centered")


@st.cache_resource
def load_assets():
    model = joblib.load(BASE / "models" / "price_model.joblib")
    opts = json.load(open(BASE / "models" / "app_options.json"))
    return model, opts


model, opts = load_assets()
cat = opts["categorical"]

st.title("🚗 Used Car Price Estimator")
st.write("Estimate a fair listing price for a used car and check whether an asking price "
         "is reasonable. Built for used-car dealers who need to price inventory quickly.")

col1, col2 = st.columns(2)
with col1:
    make = st.selectbox("Manufacturer", opts["manufacturers"])
    models_list = opts["models_by_make"].get(make, []) + ["other"]
    car_model = st.selectbox("Model", models_list)
    year = st.slider("Year", opts["year_range"][0], opts["year_range"][1], 2015)
    odometer = st.number_input("Odometer (miles)", min_value=1, max_value=500_000,
                               value=100_000, step=1000)
    cyl = st.selectbox("Cylinders", ["unknown"] + opts["cylinders"])
    state = st.selectbox("State", cat["state"], index=cat["state"].index("ca") if "ca" in cat["state"] else 0)
with col2:
    condition = st.selectbox("Condition", cat["condition"])
    fuel = st.selectbox("Fuel", cat["fuel"])
    transmission = st.selectbox("Transmission", cat["transmission"])
    drive = st.selectbox("Drive", cat["drive"])
    body = st.selectbox("Body type", cat["type"])
    color = st.selectbox("Paint colour", cat["paint_color"])
    title = st.selectbox("Title status", cat["title_status"])
    seller = st.selectbox("Seller type", cat["seller_type"])

asking = st.number_input("Asking price to check (optional, $)", min_value=0, value=0, step=500)

if st.button("Estimate price", type="primary"):
    row = pd.DataFrame([{
        "year": year, "odometer": odometer,
        "cylinders": np.nan if cyl == "unknown" else float(cyl),
        "manufacturer": make, "model": car_model, "condition": condition, "fuel": fuel,
        "transmission": transmission, "drive": drive, "type": body, "paint_color": color,
        "title_status": title, "seller_type": seller, "state": state,
    }])
    price = float(np.expm1(model.predict(row)[0]))
    low, high = price * opts["ratio_low"], price * opts["ratio_high"]

    st.metric("Estimated price", f"${price:,.0f}")
    st.write(f"Likely range (80% of past predictions): **${low:,.0f} – ${high:,.0f}**")

    if asking > 0:
        if asking > high:
            st.error("Asking price is above the expected range: likely overpriced.")
        elif asking < low:
            st.success("Asking price is below the expected range: a possible bargain, "
                       "or check for hidden problems.")
        else:
            st.info("Asking price is within the expected range.")

with st.expander("About the model"):
    m = opts["metrics"]
    st.write(
        "Model: tuned HistGradientBoosting trained on about 214,000 cleaned Craigslist "
        f"listings. On unseen data its average error is about ${m['MAE']:,} "
        f"(median error {m['median_pct_error']}%, R² {m['R2']}). "
        "Estimates are based on asking prices, not final sale prices, and are less reliable "
        "for rare or very expensive cars. Use them as a guide, not a final valuation.")
    imp = pd.Series(opts["importance"]).sort_values()
    st.write("Which inputs matter most (permutation importance):")
    st.bar_chart(imp)